#import requests
import asyncio
import aiohttp
import time
from collections import defaultdict
import json
from timeit import default_timer as timer
#import requests_cache
#from joblib import Parallel, delayed
#import multiprocessing

from biothings_explorer import BioThingsExplorer
from biothings_explorer.jsonld_processor import JSONLDHelper
from biothings_explorer.utils import property_uri_2_prefix_dict
from biothings_explorer.output_organizer import OutputOrganizor
from .basehandler import BaseHandler

#requests_cache.install_cache('biothings_cache', backend='sqlite', expire_after=36000)
bt_explorer = BioThingsExplorer()
jh = JSONLDHelper()
oo = OutputOrganizor()

def find_endpoint(input_type):
    """
    This function takes input_type, e.g. ncbigene as input, and return all endpoints which can ingest the input_type

    Return
    ======
    List of endpoints
    """
    return list(bt_explorer.api_map.successors(input_type))

async def get_json_helper(_endpoint, input_type, input_value):
    api_call_params = bt_explorer.apiCallHandler.call_api({input_type: input_value}, _endpoint)
    try:
        print('Start making API calls to {}'.format(_endpoint))
        response = await aiohttp.request('GET', api_call_params[0], params=api_call_params[1], headers={'Accept': 'application/json'})
    except:
        return {'endpoint': _endpoint, 'data': {}}
    #response = requests.get(params[0], params=params[1], headers={'Accept': 'application/json'})
    #if response.status_code == 200:
    print('Start get json output from {}'.format(_endpoint))
    json_response = await response.json()
    data = bt_explorer.apiCallHandler.preprocess_json_doc(json_response, _endpoint)
    return {'endpoint': _endpoint, 'data': data}

async def get_json(endpoints, input_type, input_value):
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
    start = time.time()
    tasks = [asyncio.ensure_future(get_json_helper(_endpoint, input_type, input_value)) for _endpoint in endpoints]
    results = await asyncio.wait(tasks)
    print("Process took: {:.2f} seconds".format(time.time() - start))
    return results
    """
    # construct API calls for each endpoint, organize them into a list
    api_call_params = []
    for endpoint_name in endpoints:
        api_call_params.append(bt_explorer.apiCallHandler.call_api({input_type: input_value}, endpoint_name))
    # use grequest to make asynchronized API calls
    rs = (grequests.get(u, params=v, headers={'Accept': 'application/json'}) for (u,v) in api_call_params)
    # get JSON output
    responses = [bt_explorer.apiCallHandler.preprocess_json_doc(api_call_response.json(), endpoint_name)
    if api_call_response.status_code == 200 else {} for api_call_response in grequests.map(rs)]
    """
    """
    # multiprocessing solution
    num_cores = multiprocessing.cpu_count()
    results = Parallel(n_jobs=num_cores)(delayed(get_json_helper)(_endpoint, input_type, input_value) for _endpoint in endpoints)
    return list(zip(endpoints, results))
    """

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
    else:
        return _value

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
    ###################################################################
    """
    This part use asyncio libary to asynchronously extract
    all the JSON outputs from individual API calls
    """
    endpoints = find_endpoint(input_type)
    ioloop = asyncio.get_event_loop()
    done, _ = ioloop.run_until_complete(get_json(endpoints, input_type, input_value))
    json_docs = []
    for fut in done:
        json_docs.append(fut.result())
    ###################################################################
    """
    This part add JSON-LD context file to individual JSON document
    """
    jsonld_docs = []
    for json_doc in json_docs:
        endpoint_name = json_doc['endpoint']
        if 'jsonld_context' in bt_explorer.registry.endpoint_info[endpoint_name]:
            jsonld_context_path = bt_explorer.registry.endpoint_info[endpoint_name]['jsonld_context']
            jsonld_docs.append(jh.json2jsonld(json_doc['data'], jsonld_context_path))
        else:
            jsonld_docs.append(None)
    ###################################################################
    """
    This part convert JSON-LD document to Nquads format
    And extract and organize the data
    """
    # rearrange the endpoints, because Asyncio will reorder the sequence
    endpoints = [_json['endpoint'] for _json in json_docs]
    # convert a list of jsonld documents to nquads documents
    nquads_list = jh.jsonld2nquads(jsonld_docs)
    outputs = defaultdict(list)
    for endpoint, nquads in list(zip(endpoints, nquads_list)):
        # get all possible associations of the endpoint
        association_list = bt_explorer.registry.endpoint_info[endpoint]['associations']
        if "@default" in nquads:
            _output = jh.fetch_properties_by_association_in_nquads(nquads["@default"], association_list)
            for _assoc, _objects in _output.items():
                for _object in _objects:
                    reorganized_data = {'endpoint': endpoint, 'api': bt_explorer.registry.endpoint_info[endpoint]['api'],
                                        'predicate': _assoc.replace('http://biothings.io/explorer/vocab/objects/', '')}
                    reorganized_data.update(oo.nquads2dict(_object))
                    object_id_prefix = reorganized_data['target']['id'].split(':')[0]
                    reorganized_data.update({'prefix': object_id_prefix})
                    object_semantic_type = bt_explorer.registry.prefix2semantictype(object_id_prefix)
                    outputs[object_semantic_type].append(reorganized_data)
    ###################################################################

    """
    property_summary = defaultdict(set)
    semantic_type_summary = defaultdict(set)
    summary = {}
    for semantic_type, pair in outputs.items():
        summary[semantic_type] = defaultdict(set)
        for _doc in pair:
            for _property, _value in _doc.items():
                if _property == 'prefix':
                    summary[semantic_type][_property].add(_value)
                elif _property in ['relation.label', 'relation.id', 'publication', 'evidence', 'object.taxonomy']:
                    if type(_value) != list:
                        if ':' in _value:
                            _prefix = _value.split(':')[0]
                            _value_no_prefix = _value[len(_prefix)+1:]
                            summary[semantic_type][_prefix].add(_value_no_prefix)
                        else:
                            summary[semantic_type][_property].add(_value)
                    else:
                        for _single_value in _value:
                            if ':' in _single_value:
                                _prefix = _single_value.split(':')[0]
                                _value_no_prefix = _single_value[len(_prefix)+1:]
                                summary[semantic_type][_prefix].add(_value_no_prefix)
                            else:
                                summary[semantic_type][_property].add(_single_value)
                elif _property not in ['object.id-secondary', 'object.label']:
                    if type(_value) != list:
                        summary[semantic_type][_property].add(_value)
                    else:
                        for _single_value in _value:
                            summary[semantic_type][_property].add(_single_value)
    for k,v in summary.items():
        for _k, _v in v.items():
            summary[k][_k] = list(_v)
    """
    return {'linkedData': outputs}
    """
        if _output:
            for _pair in _output:
                semantic_type = bt_explorer.registry.prefix2semantictype(_pair['curie'].split(':')[0])
                _pair.update({'endpoint': endpoint, 'api': bt_explorer.registry.endpoint_info[endpoint]['api'], 'prefix': _pair['curie'].split(':')[0]})
                outputs[semantic_type].append(_pair)
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
    """
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
        input_type = self.get_query_argument('input_type')
        input_value = self.get_query_argument('input_value')
        output_summary = self.get_query_argument('summary', False)
        results = exploreinput(input_type, input_value)
        if results:
            if output_summary:
                self.write(json.dumps(results))
            else:
                self.write(json.dumps({'linkedData': results['linkedData']}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "message": "No linked data could be found for " + input_type + ":" + input_value + '!'}))
