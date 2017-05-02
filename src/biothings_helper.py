from config import *
from jsonld_processor import load_context, fetch_doc_from_api, get_nquads_from_url, get_nquads_from_json, fetch_value_by_uri_relation, get_uri_value_relation
from biothings_client import ClientRedirect


def get_biothings(api, id, fields=None, fields_uri=None):
    if fields:
        doc = ClientRedirect().annotate(id, api, fields=fields)
        return doc
    elif fields_uri:
        field_name_list = uri_to_field_name(fields_uri, api)
        field_name = ",".join(field_name_list)
        doc = ClientRedirect().annotate(id, api, fields=field_name)
        return doc
    else:
        doc = ClientRedirect().annotate(id, api)
        return doc

def query_biothings(api, fields=None, fields_uri=None, fields_value=None, return_fields=None, return_fields_uri=None, fetch_all=True):
    if return_fields_uri:
        field_name_list = uri_to_field_name(return_fields_uri, api)
        return_fields = ",".join(field_name_list)    
    if fields:
        query_info = fields + ': ' + fields_value
    elif fields_uri:
        query_field_name_list = uri_to_field_name(fields_uri, api)
        query_info = compose_query_parameter_from_uri(fields_uri, fields_value, api)
    return ClientRedirect().query(api, query_info, fields=return_fields, fetch_all=fetch_all)

def find_id_from_uri(uri):
    for _id in AVAILABLE_IDS.keys():
        if AVAILABLE_IDS[_id]["uri"] == uri:
            return _id

def uri_to_field_name(uri, api, relation=None):
    context = load_context(api)
    if relation:
        return [_field for _field, _uri in context["@context"].items() if uri==_uri["@type"] and relation==_uri["@id"]]
    else:
        return [_field for _field, _uri in context["@context"].items() if uri==_uri["@type"]]

def compose_query_parameter_from_uri(uri, value, api, relation=None):
    field_name_list = uri_to_field_name(uri, api)
    print(field_name_list)
    string = ":" + value + " OR "
    if len(field_name_list) >1:
        return string.join(field_name_list)
    else:
        return (field_name_list[0] + ':' + value)

def find_annotate_api_ids(_type):
    '''
    Give an ID, look through all availalble api sources,
    if the ID can be annotated by this API, return API names in a list
    '''
    api_id = {}
    for _source in AVAILABLE_API_SOURCES:
        if "annotate_ids" in AVAILABLE_API_SOURCES[_source] and _type in AVAILABLE_API_SOURCES[_source]["annotate_ids"]:
            api_id[_source] = AVAILABLE_API_SOURCES[_source]['query_ids']
    return api_id

def find_query_api_ids(_type):
    api_id = {}
    for _source in AVAILABLE_API_SOURCES:
        if "query_syntax" in AVAILABLE_API_SOURCES[_source] and "query_ids" in AVAILABLE_API_SOURCES[_source] and _type in AVAILABLE_API_SOURCES[_source]["query_ids"]:
            api_id[_source] = AVAILABLE_API_SOURCES[_source]['annotate_ids']
    return api_id

def find_value_from_output_type(api, input, output_type, output_relation=None):
    '''
    given an api, input value
    return the value related to the uri
    '''
    url = AVAILABLE_API_SOURCES[api]['annotate_syntax'].replace("*", input)
    json_doc = fetch_doc_from_api(url)
    if json_doc:
        nquads_doc = get_nquads_from_json(json_doc, url, api)
        uri = AVAILABLE_IDS[output_type]["uri"]
        return fetch_value_by_uri_relation(nquads_doc, uri, output_relation)

def query_ids_from_output_type(api, _type, _value, input_relation=None):
    uri = AVAILABLE_IDS[_type]["uri"]
    query_info = compose_query_parameter_from_uri(uri, _value, api, input_relation)
    print(query_info)
    id_list = ClientRedirect().get_id_list(api, query_info, fetch_all=True)
    return id_list

'''
given an annotate API name and ID
find all fileds in the annotate results that
could be further linked to other APIs
'''
def find_xref(api, id):
    response = {}
    xref = {}
    if 'annotate_syntax' in AVAILABLE_API_SOURCES[api]:
        _url = AVAILABLE_API_SOURCES[api]["annotate_syntax"].replace("*", str(id))
        if 'jsonld' in AVAILABLE_API_SOURCES[api]:
            nquads_doc = get_nquads_from_url(_url, api)
            uri_value_relation = get_uri_value_relation(nquads_doc)
            response = {'url': _url, 'xref': uri_value_relation}
            return response

def find_query_id_list(api, type, value):
    _uri = AVAILABLE_IDS[type]["uri"]
    query_parameters = compose_query_parameter_from_uri(_uri, value, api)
    ids = ClientRedirect().get_id_list(api, query_parameters)
    _url = AVAILABLE_API_SOURCES[api]["query_syntax"].replace("*", query_parameters)
    results = {'type': AVAILABLE_API_SOURCES[api]['annotate_ids'][0], 'ids': ids, 'url': _url}
    return results

def find_query_id_list_for_filter(api, type, value, para):
    _uri = AVAILABLE_IDS[type]["uri"]
    query_parameters = '(' + compose_query_parameter_from_uri(_uri, value, api) + ')' + ' ' + para
    ids =  ClientRedirect().get_id_list(api, query_parameters)
    _url = AVAILABLE_API_SOURCES[api]["query_syntax"].replace("*", query_parameters)
    results = {'type': AVAILABLE_API_SOURCES[api]['annotate_ids'][0], 'ids': ids, 'url': _url}
    return results

class Biothingsexplorer():
    def __init__(self):
        self.jsonld_doc = None
        self._api_value = {}

    def get_json_doc(self, api, id):
        # construct url from id
        url = AVAILABLE_API_SOURCES[api]['annotate_syntax'].replace('*', id)
        json_doc = fetch_doc_from_api(url)
        context = load_context(api)
        json_doc.update(context)
        self.jsonld_doc = nquads_transform(json_doc)
        return json_doc

    def find_linked_apis(self):
        uri_list = get_uri_value_pairs(self.jsonld_doc)
        for _uri,_value in uri_list.items():
            _id = find_id_from_uri(_uri)
            for _api in AVAILABLE_API_SOURCES.keys():
                if _id in AVAILABLE_API_SOURCES[_api]['annotate_ids']:
                    self._api_value[_api] = _value
        print('Available APIs which could be linked out is: {}'.format(self._api_value))

    def explore_api(self, api, fields=None, fields_uri=None):
        return get_biothings(api, self._api_value[api], fields=fields, fields_uri=fields_uri)



