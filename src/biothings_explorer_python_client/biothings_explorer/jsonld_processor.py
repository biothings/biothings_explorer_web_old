import json
import requests
from pyld import jsonld
from collections import OrderedDict

from .config import AVAILABLE_API_SOURCES, AVAILABLE_IDS

def find_id_from_uri(uri):
    for _id in AVAILABLE_IDS.keys():
        if AVAILABLE_IDS[_id]["uri"] == uri:
            return _id


def fetch_doc_from_api(url):
    '''
    This function takes an uri, and call the uri
    using requests, and then return a json document
    if the call is valid
    '''
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        print("invalid uri: {}".format(url))


def is_seq(li):
    """return True if input is either a list or a tuple.
    """
    return isinstance(li, (list, tuple))


def flatten_doc(doc, outfield_sep='.', sort=True):
    ''' This function will flatten an elasticsearch document (really any json object).
        outfield_sep is the separator between the fields in the return object.
        sort specifies whether the output object should be sorted alphabetically before returning
            (otherwise output will remain in traveral order) '''

    def _recursion_helper(_doc, _ret, out):
        if isinstance(_doc, dict):
            for key in _doc:
                new_key = key if not out else outfield_sep.join([out, key])
                _recursion_helper(_doc[key], _ret, new_key)
        elif is_seq(_doc):
            for _obj in _doc:
                _recursion_helper(_obj, _ret, out)
        else:
            # this is a leaf
            _ret.setdefault(out, []).append(_doc)

    ret = {}
    new_dict = {}
    _recursion_helper(doc, ret, '')
    if sort:
        return OrderedDict(sorted([(k, v[0]) if len(v) == 1 else (k, v) for (k, v) in ret.items()], key=lambda x: x[0]))
    for (k, v) in ret.items():
        if len(v) == 1:
            new_dict[k] = v[0]
        else:
            new_dict[k] = v
    return new_dict

def load_context(api):
    '''
    load context file from a specific path
    e.g. mygene.info context file
    '''
    if 'jsonld' in AVAILABLE_API_SOURCES[api]:
        return json.loads(open(AVAILABLE_API_SOURCES[api]["jsonld"]["context_file_path"]).read())

def nquads_transform(doc):
    '''
    This function takes a json-ld document,
    and parse it into nquads format (rdf)
    '''
    t = jsonld.JsonLdProcessor()
    nquads = t.parse_nquads(jsonld.to_rdf(doc, {'format': 'application/nquads'}))['@default']
    return nquads


def jsonld_converter(json_doc, api):
    '''
    give a json doc and api name
    transform it into jsonld_format
    '''
    context = load_context(api)
    json_doc.update(context)
    return json_doc

def fetch_value_by_uri_relation(nquads, uri, relation=None):
    '''
    give a nquads and a uri,
    find all values related to this uri
    if find multiple values, return a list
    if only single value found, return the item
    '''
    value_list = []
    if relation:
        for item in nquads:
            if item['object']['datatype'] == uri and item['predicate']['value'] == relation:
                value_list.append(item['object']['value'])
    else:
        for item in nquads:
            if item['object']['datatype'] == uri:
                value_list.append(item['object']['value'])
    value = list(set(value_list))
    return value


def get_uri_list(nquads):
    '''
    give a nquads, return all available uris in it
    '''
    uri_list = list(set([_doc['object']['datatype'] for _doc in nquads]))
    return uri_list

def get_uri_value_pairs(nquads):
    uri_value_pairs = {}
    uri_list = get_uri_list(nquads)
    for _uri in uri_list:
        uri_value_pairs.update({_uri: fetch_value_by_uri_relation(nquads, _uri)})
    return uri_value_pairs

def get_uri_value_relation(nquads):
    results = [{'uri': _nquad['object']['datatype'], 'relation': _nquad['predicate']['value'], 'value': _nquad['object']['value']} for _nquad in nquads]
    results = {}
    for _nquad in nquads:
        uri = _nquad['object']['datatype']
        _id = find_id_from_uri(uri)
        relation = _nquad['predicate']['value']
        value = _nquad['object']['value']
        if _id in results:
            results[_id].append([relation, value])
        else:
            results[_id] = []
            results[_id].append([relation, value])
    return results

def get_nquads_from_url(url, api):
    json_doc = fetch_doc_from_api(url)
    json_doc = dict(flatten_doc(json_doc))
    context = load_context(api)
    json_doc.update(context)
    # jsonld doesn't recognize >
    url = url.replace('>', "&gt;")
    json_doc.update({"@id": url})
    nquads_doc = nquads_transform(json_doc)
    return nquads_doc

def get_nquads_from_json(json_doc, url, api):
    json_doc = dict(flatten_doc(json_doc))
    context = load_context(api)
    json_doc.update(context)
    # jsonld doesn't recognize >
    url = url.replace('>', "&gt;")
    json_doc.update({"@id": url})
    nquads_doc = nquads_transform(json_doc)
    return nquads_doc
