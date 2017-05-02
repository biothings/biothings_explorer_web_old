from biothings_helper import find_annotate_api_ids, find_query_api_ids, find_xref, find_query_id_list, find_query_id_list_for_filter
from config import AVAILABLE_IDS, AVAILABLE_API_SOURCES
from jsonld_processor import load_context, find_id_from_uri

node = 0
edge = 0
id_list = []

'''
initialize a cytoscape graph
reset node and edge id
'''

def initialize(_type, _id):
    global id_list
    print(_id)
    print(id_list)
    id_list = [_id]
    return node_constructor(_id, 'field_name', _type, 'field_name')
'''
Given symbol, type, kwargs info
construct the node for cytoscape
and update the node number
'''
def node_constructor(_symbol, _type, _kwargs, _kwargs_type):
    global node
    if _type == 'field_name':
        return({'data': {'id': _symbol, 'symbol': _symbol, 'type': _type, 'kwargs': _kwargs, 'kwargs_type': _kwargs_type}})
    else:
        node += 1
        return({'data': {'id': 'n' + str(node), 'symbol': _symbol, 'type': _type, 'kwargs': _kwargs, 'kwargs_type': _kwargs_type}})

'''
Given source and target id,
construct the edge for cytoscape
and update the edge number
'''
def edge_constructor(_source, _target, _relation='is_related_to'):
    global edge
    edge += 1
    return({'data': {'id': 'e' + str(edge), 'source': _source, 'target': _target, 'label': _relation}})


'''
Given node data from cytoscape
Example:
hgnc_gene_id: 1017
{'id': 'n0', 'symbol': '1017', 'type': 'field_name', 'kwargs': 'hgnc_gene_id'},
find all available apis for annotate and query related to this id
return them in the form of cytoscape nodes and edges
'''
def field_handler(data):
    add_nodes_edges = []
    _kwargs = data['symbol']
    annotate_apis = find_annotate_api_ids(data['kwargs']).keys()
    query_apis = find_query_api_ids(data['kwargs']).keys()
    if annotate_apis:
        for _api in annotate_apis:
            _node = node_constructor(_api, 'annotate_api', _kwargs, data['kwargs'])
            _edge = edge_constructor(_node['data']['id'], data['id'], 'annotate_api')
            add_nodes_edges.append(_node)
            add_nodes_edges.append(_edge)
    if query_apis:
        for _api in query_apis:
            _node = node_constructor(_api, 'query_api', _kwargs, data['kwargs'])
            _edge = edge_constructor(_node['data']['id'], data['id'], 'query_api')
            add_nodes_edges.append(_node)
            add_nodes_edges.append(_edge)
    return add_nodes_edges

def annotate_handler(data):
	_api = data['symbol']
	_id = data['kwargs']
	xref = find_xref(_api, _id)
	if xref:
		return xref

def query_handler(data):
	_api = data['symbol']
	_id = data['kwargs']
	_type = data['kwargs_type']
	query_ids = find_query_id_list(_api, _type, _id)
	return query_ids

def filter_handler(data):
    _api = data['symbol']
    _id = data['kwargs']
    _type = data['kwargs_type']
    _para = data['para']
    query_ids = find_query_id_list_for_filter(_api, _type, _id, _para)
    return query_ids

def id_handler(data):
    print(data)
    add_nodes_edges = []
    _id = data['id'].strip(' ')
    _type = data['type']
    _parent = data['parent']
    relation = data['relation']
    _node = node_constructor(_id, 'field_name', _type, 'field_name')
    print(id_list)
    print(_id)
    if _id not in id_list:
        id_list.append(_id)
        add_nodes_edges.append(_node)
    add_nodes_edges.append(edge_constructor(_node['data']['id'], _parent, relation))
    return add_nodes_edges

def relation_handler():
    add_nodes_edges = []
    relation_edge = 0
    edges= []
    for _id in AVAILABLE_IDS.keys():
        add_nodes_edges.append({'data': {'id': _id, 'type': 'id'}})
    for _api in AVAILABLE_API_SOURCES.keys():
        add_nodes_edges.append({'data': {'id': _api, 'type': 'api'}})
        if 'annotate_ids' in AVAILABLE_API_SOURCES[_api]:
            for annotate_id in AVAILABLE_API_SOURCES[_api]['annotate_ids']:
                add_nodes_edges.append({'data': {'id': relation_edge, 'source': annotate_id, 'target': _api, 'label': 'input'}})
                relation_edge += 1
        if 'jsonld' in AVAILABLE_API_SOURCES[_api]:
            context = load_context(_api)
            for k, v in context['@context'].items():
                _edge = {'data': {'source': find_id_from_uri(v["@type"]), 'target': _api, 'label': v["@id"]}}
                if _edge not in edges:
                    _edge['data']['id'] = relation_edge
                    add_nodes_edges.append(_edge)
                    edges.append(_edge)
                    relation_edge += 1
                else:
                    print(_edge)
    return add_nodes_edges

'''
Get all available ids for explore from config file
'''
def fetchid_handler():
    return list(AVAILABLE_IDS.keys())

