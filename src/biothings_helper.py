from config import *
from jsonld_processor import load_context, fetch_doc_from_api, jsonld_converter, nquads_transform, get_uri_value_pairs
from biothings_client import ClientRedirect


def find_id_from_uri(uri):
    for _id in AVAILABLE_IDS.keys():
        if AVAILABLE_IDS[_id]["uri"] == uri:
            return _id


def get_uri_list(context):
    '''
    get uri and related path ina context file
    '''
    uri_path_dict = {}
    for path, v in context.items():
        for field_name, value in v["@context"].items():
            new_path = path.replace("/", ".") + "." + field_name
            if value not in uri_path_dict:
                uri_path_dict[value] = [new_path]
            else:
                uri_path_dict[value].append(new_path)
    return uri_path_dict


def compose_query_parameter_from_uri(uri, value, api):
    context = load_context(api)
    context.pop('root')
    query_string = ''
    if uri in get_uri_list(context):
        path_list = get_uri_list(context)[uri]
        for _item in path_list:
            query_string = query_string + ' ' + _item + ':' + value + ' OR'
    return query_string.strip(' OR')

def find_id_for_xref(_id, value):
    for _source in AVAILABLE_API_SOURCES:
        if "query_ids" in AVAILABLE_API_SOURCES[_source] and _id in AVAILABLE_API_SOURCES[_source]["query_ids"]:
            return {_id: value}
        elif "annotate_ids" in AVAILABLE_API_SOURCES[_source] and _id in AVAILABLE_API_SOURCES[_source]["annotate_ids"]:
            return {_id: value}

def find_annotate_api(_type):
    '''
    Give an ID, look through all availalble api sources,
    if the ID can be annotated by this API, return API names in a list
    '''
    annotate_apis = []
    for _source in AVAILABLE_API_SOURCES:
        if "annotate_ids" in AVAILABLE_API_SOURCES[_source] and _type in AVAILABLE_API_SOURCES[_source]["annotate_ids"]:
            annotate_apis.append(_source)
    return annotate_apis

def find_query_api(_type):
    query_apis = []
    for _source in AVAILABLE_API_SOURCES:
        if "query_ids" in AVAILABLE_API_SOURCES[_source] and _type in AVAILABLE_API_SOURCES[_source]["query_ids"]:
            query_apis.append(_source)
    return query_apis

'''
given an annotate API name and ID
find all fileds in the annotate results that 
could be further linked to other APIs
'''
def find_xref(api, id):
    xref = {}
    if 'annotate_syntax' in AVAILABLE_API_SOURCES[api]:
        _url = AVAILABLE_API_SOURCES[api]["annotate_syntax"].replace("*", str(id))
        if 'jsonld' in AVAILABLE_API_SOURCES[api]:
            json_doc = fetch_doc_from_api(_url)
            jsonld_doc = jsonld_converter(json_doc, api)
            nquads = nquads_transform(jsonld_doc)
            uri_value_pairs = get_uri_value_pairs(nquads)
            for uri, value in uri_value_pairs.items():
                _id = find_id_from_uri(uri)
                if type(value) == list:
                    for _value in value:
                        if find_id_for_xref(_id, _value):
                            if _id in xref:
                                xref[_id].append(_value)
                            else:
                                xref.update({_id: [_value]})
                else:
                    if find_id_for_xref(_id, value):
                        if _id in xref:
                            xref[_id].append(value)
                        else:
                            xref.update({_id: [value]})
            return xref

def find_query_id_list(api, type, value):
	_uri = AVAILABLE_IDS[type]["uri"]
	query_parameters = compose_query_parameter_from_uri(_uri, value, api)
	return ClientRedirect().get_id_list(api, query_parameters, fetch_all=False)

