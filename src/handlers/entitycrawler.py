import requests
import grequests
from collections import defaultdict
import json
from timeit import default_timer as timer
import requests_cache
from joblib import Parallel, delayed
import multiprocessing

from biothings_explorer import BioThingsExplorer
from biothings_explorer.jsonld_processor import json2jsonld, jsonld2nquads
from .basehandler import BaseHandler

requests_cache.install_cache('biothings_cache', backend='sqlite', expire_after=36000)
bt_explorer = BioThingsExplorer()

def find_endpoint(input_type):
    """
    This function takes input_type as input, and return all endpoints which can ingest the input_type

    Return
    ======
    List of endpoints
    """
    return list(bt_explorer.api_map.successors(input_type))

def get_json_helper(_endpoint, input_type, input_value):
    params = bt_explorer.apiCallHandler.call_api({input_type: input_value}, _endpoint)
    response = requests.get(params[0], params=params[1], headers={'Accept': 'application/json'})
    if response.status_code == 200:
        return bt_explorer.apiCallHandler.preprocess_json_doc(response.json(), _endpoint)
    else:
        return {}

def get_json(endpoints, input_type, input_value):
    """
    Given endpoint_name as a list, input_type and input_value,
    Make API calls for each pair of (endpoint, input_type, input_value),
    Return JSON output from the API call

    Return
    ======
    List of (endpoint, JSON output)
    """
    # this code transform prefix to URI
    input_type = bt_explorer.registry.prefix2uri(input_type)
    """
    # construct API calls for each endpoint, organize them into a list
    api_call_params = []
    for endpoint_name in endpoints:
        api_call_params.append(bt_explorer.apiCallHandler.call_api({input_type: input_value}, endpoint_name))
    # use grequest to make asynchronized API calls
    rs = (grequests.get(u, params=v, headers={'Accept': 'application/json'}) for (u,v) in api_call_params)
    # get JSON output
    responses = [bt_explorer.apiCallHandler.preprocess_json_doc(api_call_response.json(), endpoint_name) if api_call_response.status_code == 200 else {} for api_call_response in grequests.map(rs)]
    """
    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(get_json_helper)(_endpoint, input_type, input_value) for _endpoint in endpoints)
    return list(zip(endpoints, results))

def uri2curie(URI):
    """
    Given an URI, e.g. http://identifiers.org/ncbigene/1017
    Return it in CURIE format, e.g. NCBIGene:1017

    Return
    ======
    CURIE
    """
    _value = URI.split('/')[-1]
    _uri = URI[:len(URI)-len(_value)]
    if _uri in bt_explorer.registry.bioentity_info:
        prefix = bt_explorer.registry.bioentity_info[_uri]['preferred_name']
        return (prefix + ':' + _value)

def extractnquads(nquads):
    """
    Given an nquads doc
    Extract the predicate and object info
    For object URI, convert it into CURIE format, e.g. http://identifiers.org/ncbigene/1017 --> NCBIGene:1017
    For predicate, convert it from URI to normal text, e.g. http://biothings.io/ontology/targets --> targets

    Return
    ======
    List of (CURIE, RELATION)
    """
    if not nquads:
        return None
    if "@default" not in nquads:
        return None
    # Loop through each nquad
    pairs = []
    for _nquad in nquads["@default"]:
         if not _nquad['object']['value'].startswith('_:'):
            _object = _nquad['object']['value']
            _predicate = _nquad['predicate']['value']
            curie = uri2curie(_object)
            if curie:
                pairs.append({'curie': curie, 'predicate': _predicate.split('/')[-1]})
    return pairs


def exploreinput(input_type, input_value):
    """
    Main function
    Takes an input_type, input_value,
    crawling all API endpoints taking the input
    Return all bio-entities related to this input

    Return
    ======
    List of (CURIE, RELATION, Endpoint, API)
    """
    start = timer()
    endpoints = find_endpoint(input_type)
    end = timer()
    print('Amount of time used for finding endpoints is : {}'.format(end - start))
    start = timer()
    json_docs = get_json(endpoints, input_type, input_value)
    end = timer()
    print('Amount of time used for making API calls and retrieving JSON docs is : {}'.format(end - start))
    jsonld_docs = []
    start = timer()
    for json_doc in json_docs:
        endpoint_name = json_doc[0]
        if 'jsonld_context' in bt_explorer.registry.endpoint_info[endpoint_name]:
            jsonld_context_path = bt_explorer.registry.endpoint_info[endpoint_name]['jsonld_context']
            jsonld_docs.append(json2jsonld(json_doc[1], jsonld_context_path))
        else:
            jsonld_docs.append(None)
    end = timer()
    print('Amount of time used for adding JSON-LD context is : {}'.format(end - start))
    start = timer()
    nquads_list = jsonld2nquads(jsonld_docs)
    end = timer()
    print('Amount of time used for converting JSON docs to Nquads is : {}'.format(end - start))
    outputs = defaultdict(list)
    start = timer()
    for endpoint, nquads in list(zip(endpoints,nquads_list)):
        _output = extractnquads(nquads)
        if _output:
            for _pair in _output:
                semantic_type = bt_explorer.registry.prefix2semantictype(_pair['curie'].split(':')[0])
                _pair.update({'endpoint': endpoint, 'api': bt_explorer.registry.endpoint_info[endpoint]['api'], 'prefix': _pair['curie'].split(':')[0]})
                outputs[semantic_type].append(_pair)
    end = timer()
    print('Amount of time used for orgainze linked data information is : {}'.format(end - start))
    summary = {}
    start = timer()
    for semantic_type, pair in outputs.items():
        summary[semantic_type] = defaultdict(set)
        for _doc in pair:
            summary[semantic_type]['api'].add(_doc['api'])
            summary[semantic_type]['endpoint'].add(_doc['endpoint'])
            summary[semantic_type]['predicate'].add(_doc['predicate'])
            summary[semantic_type]['id'].add(_doc['curie'].split(':')[0])
    for k,v in summary.items():
        for _k, _v in v.items():
            summary[k][_k] = list(_v)
    end = timer()
    print('Amount of time used for organizing summary is : {}'.format(end - start))
    results = {'summary': summary, 'linkedData': outputs}
    return results

class Crawler(BaseHandler):
    """
    This function serves as one BioThings Explorer API endpoint
    Given an input_type and input_value, 
    return all biological entities(type & value) which could be linked to this entity

    Params
    ======
    DefaultDict grouped by semantic type

    """
    def get(self):
        input_type = self.get_argument('input_type')
        input_value = self.get_argument('input_value')
        results = exploreinput(input_type, input_value)
        if results:
            self.write(json.dumps(results))