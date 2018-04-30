from pyld import jsonld
import json
import re
import requests
import grequests
from collections import defaultdict
from subprocess import Popen, PIPE, STDOUT
from joblib import Parallel, delayed
import multiprocessing
import logging

logger = logging.getLogger(__name__)

from .utils import readFile

class JSONLDHelper:
    def __init__(self):
        self.processor = jsonld.JsonLdProcessor()
        self.temp_attr_id = None

    def jsonld2nquads_helper(self, jsonld_doc):
        """
        Given a JSONLD document, return its nquads format

        Params
        ======
        jsonld_doc: jsonld document containing both JSON and the context file

        TODO
        ======
        Currently it relies on the JSONLD ruby client to convert to nquads
        When the JSONLD Python client is ready to adapt to 1.1, 
        should switch to the Python client
        """
        """
        No longer need JSON-LD Ruby Client
        PyLD for 1.1 json-ld version is available
        # the following 6 lines use JSON-LD Ruby client to convert
        # JSON-LD document into NQuads format
        cmd = 'jsonld --validate --format nquads'
        p = Popen(cmd.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.stdin.write(doc.encode('utf-8'))
        stdout_data = p.communicate()[0]
        p.stdin.close()
        _response = stdout_data.decode()
        """
        # convert from jsonld doc to nquads format
        nquads = jsonld.to_rdf(jsonld_doc, {'format': "application/nquads"})
        """
        No longer need to deal with ruby error message
        if _response.startswith(('Error', 'ERROR')):
            logger.error("An error occured when JSON-LD Ruby client tries to parse the JSON-LD. \
                         The first 100 chars of the JSON document is %s", jsonld_doc[:100])
            return None
        # deal with cases when JSON-LD Ruby client returns empty resutls
        elif _response.startswith('\nParsed 0 statements'):
            logger.warning("0 statements is found when JSON-LD Ruby client tries to parse the JSON-LD input.\
                           The first 100 chars of the JSON document is %s", jsonld_doc[:100])
        else:
        """
        try:
            return self.processor.parse_nquads(nquads)
        except Exception as e:
            logger.error("Something Unexpected happend when JSON-LD Python client tries to parse the JSON-LD. \
                         The first 100 chars of the JSON document is %s", json.dumps(jsonld_doc[:100]))
            logger.error(e, exc_info=True)
            return None

    def jsonld2nquads(self, jsonld_docs):
        """
        Given a JSON-LD annotated document,
        Fetch it's corresponding NQUADs file from JSON-LD playground
        'http://jsonld.biothings.io/?action=nquads'

        TODO: Currently, PyLD hasn't been updated to match JSON-LD v 1.1
        So we are using the JSON-LD playground API, which is built upon
        JSON-LD ruby client for 1.1 version. When PyLD has been updated to
        match 1.1, we should switch back to PyLD.

        Params
        ======
        jsonld_doc: (dict)
            JSON-LD annotated document
        """
        # handle cases where input is a list of JSON documents
        # in this case, the results will also be a list of NQuads parsing results
        if type(jsonld_docs) == list and type(jsonld_docs[0]) == dict:
            #results = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(self.jsonld2nquads_helper)(_doc) for _doc in jsonld_docs)
            results = []
            for _doc in jsonld_docs:
                results.append(self.jsonld2nquads_helper(_doc))
            if len(results) == 1:
                return results[0]
            else:
                return results
        # handle cases where input is a single JSON object document
        # in this case, the results will be a single NQuads parsing result
        elif type(jsonld_docs) == dict:
            """
            jsonld_docs = [jsonld_docs]
            results = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(self.jsonld2nquads_helper)(_doc) for _doc in jsonld_docs)
            return results[0]
            """
            return self.jsonld2nquads_helper(jsonld_docs)
        # if the input is neither list of json_docs nor single json_doc
        # log error message and return None
        else:
            logger.warning("The input of the jsonld2nquads function should be a list of JSON docs or a single JSON dictionary doc. \
                           You input is %s. The first 100 chars of the input is %s", type(jsonld_docs), jsonld_doc[:100])
            return None

    def json2jsonld(self, json_docs, jsonld_context_path):
        """
        Given a JSON document and the endpoint where the doc comes from
        Fetch the JSON-LD context file for the endpoint
        Apply the JSON-LD context to JSON file to construct the JSON-LD document

        Return
        ======
        JSON-LD document
        """
        jsonld_context = readFile(jsonld_context_path)
        if type(json_docs) == list and type(json_docs[0]) == dict:
            jsonld_docs = [json_doc.update(jsonld_context) for json_doc in json_docs]
            return json_docs
        elif type(json_docs) == dict:
            json_docs.update(jsonld_context)
            return json_docs
        else:
            logger.warning("The input of the json2jsonld function should be a list of JSON docs or a single JSON dictionary doc. \
                           You input is %s. The first 100 chars of the input is %s", type(jsonld_docs), jsonld_doc[:100])
            return None

    def json2nquads(self, json_docs, context_file_path):
        """
        Given a JSON document, perform the following actions
        1) Find the json-ld context file based on endpoint_name
        2) Add JSON-LD context file to JSON doc
        3) Convert the JSON-LD doc into N-quads format

        Params
        ======
        json_doc: (dict)
            JSON document fetched from API calls
        endpoint_name: (str)
            the endpoint which the JSON doc comes from
        output: (str)
            URI subject
        predicate:
            NQUADS predicate, default is None
        """
        jsonld_docs = self.json2jsonld(json_docs, context_file_path)
        nquads = self.jsonld2nquads(jsonld_docs)
        return nquads

    def find_object_properties_in_jsonld(self, _dict):
        """
        extract the @base field corresponding to "attr:id" in a nested JSON-LD context file
        """
        for k,v in _dict.items():
            # check if @id startswith "attr:" or "rel:"
            if isinstance(v, dict) and "@id" in v and v["@id"] == "attr:id":
                # @base should be in the child level of @context
                if "@base" in v["@context"]:
                    self.temp_attr_id = v["@context"]["@base"]
                else:
                    print('@base should be included here! Something wrong with the JSON-LD context file!!')
            # otherwise, recall this function to look into the child level
            elif isinstance(v, dict):
                self.find_object_properties_in_jsonld(v)

    def jsonld_parser_helper(self, _dict, relation=defaultdict(set)):
        """
        extract relationship information from "@id" which startsfrom "assoc:"
        extract output information from "@base"
        """
        for k, v in _dict.items():
            # First, looking for value of @id startswith "assoc"
            # this represents an association in the nested structure
            if isinstance(v, dict) and "@id" in v and v["@id"].startswith("assoc:"):
                # Next, looking for whether "@base" exists in the direct child level
                if "@context" in v and "@base" in v["@context"]:
                    relation[v["@context"]["@base"]].add(v["@id"])
                # If "@base" not exists in direct child level, look for levels deeper
                elif "@context" in v:
                    self.temp_attr_id = None
                    self.find_object_properties_in_jsonld(v["@context"])
                    if self.temp_attr_id:
                        relation[self.temp_attr_id].add(v["@id"])
                    else:
                        print("attr:id is missing in the object properties!")
            elif isinstance(v, dict):
                self.jsonld_parser_helper(v, relation=relation)
        return relation

    def jsonld_relation_parser(self, jsonld_context):
        """
        Given a JSON-LD context file, reorganize the file
        so that the key would be the attr id,
        the rest of the information would be wrapped in the value

        Example Outputs:

        >>> jsonld_helper = JSONLDHelper()
        >>> jsonld_context_file = {"hits": {"@id": "http://bt.d2g/", "@type": "@id", "@context": {"gene": {"@id": ""}}}
        }}

        """
        if type(jsonld_context) != dict or '@context' not in jsonld_context:
            logging.error("Invalid JSON-LD context file!")
            return
        return self.jsonld_parser_helper(jsonld_context, relation=defaultdict(set))

    def fetch_object_value_by_predicate_value_in_nquads(self, nquads, predicate_value):
        """
        Given a nquads parsing results and a predicate_value
        find the corresponding object value(s)
        """
        object_values = []
        if '@default' in nquads:
            nquads = nquads['@default']
        for _nquad in nquads:
            if _nquad['predicate']['value'] == predicate_value:
                object_values.append(_nquad['object']['value'])
        return object_values

    def fetch_object_and_predicate_value_by_subject_value_in_nquads(self, nquads, subject_value, results=None):
        """
        Given a nquads parsing results and a subject_value
        find the corresponding object and predicate value
        """
        if not results:
            results = defaultdict(list)
        if '@default' in nquads:
            nquads = nquads['@default']
        for _nquad in nquads:
            if _nquad['subject']['value'] == subject_value:
                current_predicate_value = _nquad['predicate']['value']
                current_object_value = _nquad['object']['value']
                if current_predicate_value != 'http://biothings.io/pass/':
                    results[current_predicate_value].append(_nquad['object']['value'])
                else:
                    results = self.fetch_object_and_predicate_value_by_subject_value_in_nquads(nquads, _nquad['object']['value'], results)
        return results

    def fetch_properties_by_association_in_nquads(self, nquads, association_list):
        results = {}
        for _association in association_list:
            results[_association] = []
            object_values = self.fetch_object_value_by_predicate_value_in_nquads(nquads, _association)
            for _object_value in object_values:
                if _object_value.startswith('_:'):
                    object_predicate_dict = self.fetch_object_and_predicate_value_by_subject_value_in_nquads(nquads, _object_value)
                    if object_predicate_dict:
                        results[_association].append(object_predicate_dict)
                    else:
                        print("Could not fetch any properties from the given association: {}".format(_object_value))
                else:
                    results[_association].append({'http://biothings.io/explorer/vocab/attributes/id': [_object_value]})
        return results

    def fetch_properties_by_association_and_prefix_in_nquads(self, nquads, association, prefix):
        association_results = self.fetch_properties_by_association_in_nquads(nquads, [association])
        association_and_prefix_results = [_doc for _doc in association_results[association] if _doc['http://biothings.io/explorer/vocab/attributes/id'][0].startswith(prefix)]
        return association_and_prefix_results

t = jsonld.JsonLdProcessor()

def process_jsonld(doc):
    # cmd = 'ruby jsonld_test_cli.rb -a compact'
    doc = json.dumps(doc)
    logger.debug('The JSONLD file after json.dumps is %s', doc)
    RUBY_JSONLD_CMD = 'jsonld'
    cmd = RUBY_JSONLD_CMD + ' '
    cmd += '--validate --format nquads'
    p = Popen(cmd.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p.stdin.write(doc.encode('utf-8'))
    # stdout_data = p.communicate(input=doc.encode('utf-8'))[0]
    stdout_data = p.communicate()[0]
    p.stdin.close()
    _response = stdout_data.decode()
    if 'Parsed' in _response:
        _nquad = re.sub('Parsed .*second.\n', '', _response)
        return t.parse_nquads(_nquad)
    else:
        return None

def json2jsonld(json_doc, jsonld_context_path):
    """

    """
    doc = json.dumps(doc).replace(' ', '')
    cmd = 'jsonld --validate --format nquads'
    p = Popen(cmd.split(), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    p.stdin.write(doc.encode('utf-8'))
    stdout_data = p.communicate()[0]
    p.stdin.close()
    _response = stdout_data.decode()
    # check if startswith 'ERROR'
    # check if return nquads
    # check if the nquads is empty
    # if parsing error
    if 'Parsed' in _response:
        _nquad = re.sub('Parsed .*second.\n', '', _response)
        return t.parse_nquads(_nquad)
    else:
        return None

'''
def jsonld2nquads(jsonld_doc, mode='batch'):
    """
    Given a JSON-LD annotated document,
    Fetch it's corresponding NQUADs file from JSON-LD playground
    'http://jsonld.biothings.io/?action=nquads'

    TODO: Currently, PyLD hasn't been updated to match JSON-LD v 1.1
    So we are using the JSON-LD playground API, which is built upon
    JSON-LD ruby client for 1.1 version. When PyLD has been updated to
    match 1.1, we should switch back to PyLD.

    Params
    ======
    jsonld_doc: (dict)
        JSON-LD annotated document
    """
    # need to skip html escapes
    if mode != 'batch':
        nquads = requests.post('http://jsonld.biothings.io/?action=nquads', data={'doc': json.dumps(jsonld_doc).replace('>', "&gt;").replace(' ', '')})
        if nquads.status_code != 413:
            # remove the log line from the nquads
            nquads = re.sub('Parsed .*second.\n', '', nquads.json()['output'])
            return t.parse_nquads(nquads)
    elif mode == 'batch':
        responses = []
        for _jsonld_doc in jsonld_doc:
            responses.append(grequests.post('http://jsonld.biothings.io/?action=nquads', data={'doc': json.dumps(_jsonld_doc).replace('>', "&gt;").replace(' ', '')}))
        responses = grequests.map(iter(responses))
        results = []
        for _response in responses:
            if _response.status_code != 413:
                nquads = re.sub('Parsed .*second.\n', '', _response.json()['output'])
                results.append(t.parse_nquads(nquads))
            else:
                results.append(None)
        return results
'''
def jsonld2nquads(jsonld_docs):
    """
    Given a JSON-LD annotated document,
    Fetch it's corresponding NQUADs file from JSON-LD playground
    'http://jsonld.biothings.io/?action=nquads'

    TODO: Currently, PyLD hasn't been updated to match JSON-LD v 1.1
    So we are using the JSON-LD playground API, which is built upon
    JSON-LD ruby client for 1.1 version. When PyLD has been updated to
    match 1.1, we should switch back to PyLD.

    Params
    ======
    jsonld_doc: (dict)
        JSON-LD annotated document
    """
    results = []
    """
    for _doc in jsonld_docs:
        _response = process_jsonld(_doc)
        if 'Parsed' in _response:
            _nquad = re.sub('Parsed .*second.\n', '', _response)
            results.append(t.parse_nquads(_nquad))
        else:
            results.append(None)
    """
    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(process_jsonld)(_doc) for _doc in jsonld_docs)
    return results


def fetchvalue(nquads, object_uri, predicate=None):
    """
    Given a NQUADS together with (URI/subject, predicate) pair
    Extract the object value

    Params
    ======
    nquads: (list)
        NQUADS doc
    object_uri: (str)
        URI subject
    predicate:
        NQUADS predicate. If None is specified, return all objects matching the subject
    """
    results = []
    # check if it's a valid nquads
    if nquads and '@default' in nquads:
        for _nquad in nquads['@default']:
            if predicate and object_uri in _nquad['object']['value'] and _nquad['predicate']['value'].split('/')[-1] == predicate.split(':')[-1]:
                results.append((_nquad['object']['value'].split(object_uri)[1], _nquad['predicate']['value'].split('/')[-1]))
            elif not predicate and object_uri in _nquad['object']['value']:
                results.append((_nquad['object']['value'].split(object_uri)[1], _nquad['predicate']['value'].split('/')[-1]))
    elif nquads:
        print('This is a invalid nquads, missing "@default"!!!')
    else:
        print('The nquads is empty')
    # if results is empty, it could be either nquads is empty or object_uri could not be found in nuqads
    if results:
        return list(set(results))
    else:
        return

def find_base(d, relation=defaultdict(set)):
    """
    Iterative function
    Given a JSON-LD context file as Python Dictionary,
    return all bio-entity URIs in that context file
    together with the relationship(s) as a set
    e.g. {'http://identifiers.org/pdb/': {'ont:has3DStructure'}}

    Params
    ======
    d: (dict)
        JSON-LD context
    relation: (dict)
        temporarily store relation info
    """
    for k, v in d.items():
        if isinstance(v, dict) and "@context" in v and "@base" in v["@context"]:
            relation[v["@context"]["@base"]].add(v["@id"])
        # if v is a dict and doesnt have @base, then reiterative the process
        elif isinstance(v, dict):
            find_base(v, relation=relation)
    return relation

def json2nquads(json_doc, context_file_path, output_type, predicate=None):
    """
    Given a JSON document, perform the following actions
    1) Find the json-ld context file based on endpoint_name
    2) Add JSON-LD context file to JSON doc
    3) Convert the JSON-LD doc into N-quads format

    Params
    ======
    json_doc: (dict)
        JSON document fetched from API calls
    endpoint_name: (str)
        the endpoint which the JSON doc comes from
    output: (str)
        URI subject
    predicate:
        NQUADS predicate, default is None
    """
    context_file = readFile(context_file_path)
    for _json_doc in json_doc:
        _json_doc.update(context_file)
    nquads = jsonld2nquads(json_doc)
    results = []
    for _nquad in nquads:
        output = fetchvalue(_nquad, output_type, predicate=predicate)
        if output:
            outputs = list(set(output))
            results.append(outputs)
        else:
            results.append(None)
    return results
