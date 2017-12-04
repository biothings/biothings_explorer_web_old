from pyld import jsonld
import json
import re
import requests
from collections import defaultdict

from .utils import readFile


t = jsonld.JsonLdProcessor()


def jsonld2nquads(jsonld_doc):
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
    nquads = requests.post('http://jsonld.biothings.io/?action=nquads', data={'doc': json.dumps(jsonld_doc).replace('>', "&gt;").replace(' ', '')})
    if nquads.status_code != 413:
        # remove the log line from the nquads
        nquads = re.sub('Parsed .*second.\n', '', nquads.json()['output'])
        return t.parse_nquads(nquads)

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

def json2nquads(json_doc, context_file_path, output, predicate=None):
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
    json_doc.update(context_file)
    nquads = jsonld2nquads(json_doc)
    output = fetchvalue(nquads, output, predicate=predicate)
    if output:
        outputs = list(set(output))
        return outputs
    else:
        return None
