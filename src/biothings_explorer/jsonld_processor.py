from pyld import jsonld
import json
import re
from collections import defaultdict
from subprocess import Popen, PIPE, STDOUT
import multiprocessing
import time

from .context import get_logger
#logger.info('number of cpus is %s', multiprocessing.cpu_count())

from .utils import readFile

class JSONLDHelper:
    def __init__(self):
        self.processor = jsonld.JsonLdProcessor()
        self.temp_attr_id = None
        self.temp_properties = None
        self.logger, self.logfile = get_logger('jsonld')

    def jsonld2nquads_helper(self, jsonld_doc):
        """
        Given a JSONLD document, return its nquads format

        Params
        ======
        jsonld_doc: jsonld document containing both JSON and the context file
        """
        # convert from jsonld doc to nquads format
        try:
            nquads = jsonld.to_rdf(jsonld_doc, {'format': "application/nquads"})
            return self.processor.parse_nquads(nquads)
        except Exception as e:
            (self.logger.error("Something Unexpected happend when JSON-LD Python client tries to parse the JSON-LD.\
                         The first 100 chars of the JSON document is %s", json.dumps(jsonld_doc)[:100]))
            self.logger.error(e, exc_info=True)
            return None

    def jsonld2nquads(self, jsonld_docs, alwayslist=False):
        """
        Given a JSON-LD annotated document,
        Fetch it's corresponding NQUADs file

        Params
        ======
        jsonld_docs: (dict or list of dicts)
            A single or a list of JSON-LD annotated document(s)
        """
        # handle cases where input is a list of JSON documents
        # in this case, the results will also be a list of NQuads parsing results
        if type(jsonld_docs) == list and type(jsonld_docs[0]) == dict:
            #results = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(self.jsonld2nquads_helper)(_doc) for _doc in jsonld_docs)
            results = []
            for i, _doc in enumerate(jsonld_docs):
                results.append(self.jsonld2nquads_helper(_doc))
            if len(results) == 1 and alwayslist == False:
                return results[0]
            else:
                return results
        # handle cases where input is a single JSON object document
        # in this case, the results will be a single NQuads parsing result
        elif type(jsonld_docs) == dict:
            if alwayslist == False:
                return self.jsonld2nquads_helper(jsonld_docs)
            else:
                return [self.jsonld2nquads_helper(jsonld_docs)]
        # if the input is neither list of json_docs nor single json_doc
        # log error message and return None
        else:
            self.logger.error("jsonld2nquads only takes a single or list of JSON doc(s). You input is %s. The first 100 chars of the input is %s" %(type(jsonld_docs), json.dumps(jsonld_docs)[:100]))
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
                    logger.info('@base should be included here! Something wrong with the JSON-LD context file!!')
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
                        logger.warn("attr:id is missing in the object properties!")
            elif isinstance(v, dict):
                self.jsonld_parser_helper(v, relation=relation)
        return relation

    def extract_predicates_from_jsonld(self, _dict, predicates=set()):
        """
        Look for all unique values in "@id" field within JSON-LD context files
        """
        for k, v in _dict.items():
            if isinstance(v, dict):
                self.extract_predicates_from_jsonld(v, predicates=predicates)
            elif k == "@id":
                predicates.add(v)
        return predicates

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
        if nquads and '@default' in nquads:
            nquads = nquads['@default']
            for _nquad in nquads:
                if _nquad['predicate']['value'] == predicate_value:
                    object_values.append(_nquad['object']['value'])
            return object_values
        else:
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
            #logger.info('object_values: %s', object_values)
            for _object_value in object_values:
                #logger.info('currently processing object_value: %s', _object_value)
                if _object_value.startswith('_:'):
                    object_predicate_dict = self.fetch_object_and_predicate_value_by_subject_value_in_nquads(nquads, _object_value)
                    #logger.info('current object_predicate_dict is %s', object_predicate_dict)
                    if object_predicate_dict:
                        results[_association].append(object_predicate_dict)
                    else:
                        logger.warn("Could not fetch any properties from the given association: {}".format(_object_value))
                else:
                    results[_association].append({'http://biothings.io/explorer/vocab/attributes/id': [_object_value]})
        print(results)
        return results

    def fetch_properties_by_association_and_prefix_in_nquads(self, nquads, association, prefix):
        association_results = self.fetch_properties_by_association_in_nquads(nquads, [association])
        association_and_prefix_results = [_doc for _doc in association_results[association] if 'http://biothings.io/explorer/vocab/attributes/id' in _doc and _doc['http://biothings.io/explorer/vocab/attributes/id'][-1].startswith(prefix)]
        return association_and_prefix_results

    def locate_association_in_jsonld_context_file(self, jsonld_context, association):
        if "@context" in jsonld_context:
            content = jsonld_context['@context']
            for k, v in content.items():
                if type(v) != dict:
                    pass
                elif "@id" in v and v["@id"] == association:
                    self.temp_properties = v["@context"]
                else:
                    self.locate_association_in_jsonld_context_file(v, association)
    
    def organize_properties_in_jsonld_context_file(self, properties):
        for k, v in properties.items():
            if type(v) != dict:
                pass
            elif "@id" in v and (v["@id"].startswith("attr") or v["@id"].startswith("rel")):
                _key = v["@id"]
                _key = _key.replace('attr', 'object').replace('rel', 'edge')
                self.organized_properties[_key] = v["@context"]["@base"]
            elif k == "@base":
                self.organized_properties["node:id"] = v
            else:
                self.organize_properties_in_jsonld_context_file(v)

    def fetch_properties_for_association_in_jsonld_context_file(self, jsonld_context, association):
        self.locate_association_in_jsonld_context_file(jsonld_context, association)
        if self.temp_properties:
            self.organized_properties = {}
            self.organize_properties_in_jsonld_context_file(self.temp_properties)
            return self.organized_properties
