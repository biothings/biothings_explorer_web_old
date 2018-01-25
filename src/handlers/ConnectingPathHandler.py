import json
import operator
from collections import defaultdict
from .basehandler import BaseHandler
import os, sys
from os import path
import networkx as nx

lib_path = os.path.abspath(os.path.join('..', 'biothings_explorer'))
sys.path.append( path.dirname( path.dirname( path.abspath(lib_path))))
from biothings_explorer import BioThingsExplorer

bt_explorer = BioThingsExplorer()

color_dict = {'ClinicalTrial': 'rgba(144, 144, 28, 0.4)', 'Gene': 'rgba(55, 230, 84, 0.93)', 
              'Drug': 'rgba(230, 55, 218, 0.93)', 'Protein': 'rgba(55, 227, 230, 0.6)', 
              'Allele/Variant': 'rgba(230, 174, 55, 0.83)', 'ExperimentalStudy': 'rgba(86, 28, 144, 0.3)',
              'Phenotype': 'rgba(28, 86, 144, 0.3)', 'Pathway': 'rgba(230, 55, 116, 0.63)',
              'Disease': 'rgba(166, 55, 230, 0.84)', 'Reaction': 'rgba(100, 88, 77, 0.4)'}

def label2color(label):
    uri = bt_explorer.registry.prefix2uri(label)
    if uri:
        return color_dict[bt_explorer.registry.bioentity_info[uri]['semantic type']]
    else:
        return "rgba(250, 0, 0, 1.0)"

def find_edge_label(G, source, target, relation=None):
    """
    Given a MultiDiGraph, together with a source, target pair
    Return the edge label info associated with the (source, target) pair
    1) If only one label exists, return the label
    2) When multiple label exists, if relation parameter is in the label(s), return the relation parameter
    3) If relation parameter not in the labels, return None

    Parmas
    ======
    G: (multiDiGraph)
        a multiDiGraph containaing nodes, edges and labels
    source: (multiDiGraph node)
    target: (multiDiGraph node)
    relation:
        The label given by user, default is None

    Return
    ======
        label info for the source target pair
    """
    if (source, target) not in G.edges():
        print('The given pair source-target pair ({}, {}) is not in the graph!'.format(source, target))
        return None
    edge_labels = [v['label'] for k, v in G.get_edge_data(source, target).items()]
    if len(edge_labels) == 1:
        return edge_labels[0]
    elif len(edge_labels) > 1 and not relation:
        return edge_labels
    elif len(edge_labels) > 1 and relation and relation in edge_labels:
        return relation
    else:
        return None

###########################################################################
# Sample Input: (
#                 [('ncbigene', 'http://mygene.info/v1/'),
#                  ('ncbigene', 'http://myvariant.info/v1/'),
#                  ('http://mygene.info/v1/', 'hgnc.symbol'),
#                  ('http://myvariant.info/v1/', 'hgnc.symbol')])
# The input is the edges returned from networkx
# We need to take the input and feed it into plotly sankey plot
# The output which plotly sankey plot accepts looks like this:
# Sample Output: 
# {
#    "label": ["ncbigene", "MyGene.info/v1/query", 
#             "MyVariant.info/v1/query", "hgnc.symbol"],
#   "source": [0, 0, 1, 2], # represent the index in label
#    "target": [1, 2, 3, 3],
#    "value": [1,1,1,1] # edge weight, this doesn't apply for our use case
# }    
# Issue: plotly fails to work if there are too many nodes
###########################################################################    
def networkx_to_plotly(edges, duplicates_not_allowed=[]):
    input_list = []
    output_list = []
    # initialize the output json doc
    output_json = {'labels': [], 'colors': [], 'source': [], 'target': [], 'value': [], 'edge_labels': []}
    # loop through each edge, load the first element into source
    # and load the second element into target
    # load all unique elements to the nodes
    idx = 0
    input_idx = {}
    output_idx = {}
    for _edge in edges:
        if _edge[0] in duplicates_not_allowed:
            if _edge[0] not in output_json['labels']:
                input_idx[_edge[0]] = idx
                output_idx[_edge[0]] = idx
                idx += 1
                output_json['labels'].append(_edge[0])
                output_json['colors'].append(label2color(_edge[0]))
        elif _edge[0] not in input_idx:
            input_idx[_edge[0]] = idx
            idx += 1
            output_json['labels'].append(_edge[0])
            output_json['colors'].append(label2color(_edge[0]))
        output_json['source'].append(input_idx[_edge[0]])
        if _edge[1] in duplicates_not_allowed:
            if _edge[1] not in output_json['labels']:
                input_idx[_edge[1]] = idx
                output_idx[_edge[1]] = idx
                idx += 1
                output_json['labels'].append(_edge[1])
                output_json['colors'].append(label2color(_edge[1]))
        elif _edge[1] not in output_idx:
            output_idx[_edge[1]] = idx
            idx += 1
            output_json['labels'].append(_edge[1])
            output_json['colors'].append(label2color(_edge[1]))
        output_json['target'].append(output_idx[_edge[1]])
        output_json['edge_labels'].append(_edge[2])
        if type(_edge[2]) == list:
            output_json['value'].append(1*len(_edge[2]))
        else:
            output_json['value'].append(1)
    return output_json

###########################################################################   
# This function checks whether a node belongs to a specific data type, 
# e.g. api, endpoint, or bio-entity
# input: node_name
# output: {id: node_name, type: data_type}
###########################################################################  
def construct_cytoscape_node(node, entity_list=[], api_list=[], endpoint_list=[]):
    if node in entity_list:
        return {"data": {"id": node, "type": "bio-entity", "level": 2}}
    elif node in api_list:
        return {"data": {"id": node, "type": "api", "level": 0}}
    elif node in endpoint_list:
        return {"data": {"id": node, "type": "endpoint", "level": 1}}
    else:
        return {"data": {"id": node, "type": "value"}}

###########################################################################   
# This function takes a edge in the form of tuple, and convert it to the 
# form accepted by cytoscape.js 
# Sample input: (node1, node2)
# Sample output: {"data": {"source": node1, "target": node2}}
########################################################################### 
def construct_cytoscape_edge(edge, _id=None, level = 0):
    result = {"data": {"source": edge[0], "target": edge[1]}}
    if _id:
        result['data']['label'] = _id
    if level != 0:
        result['group'] = 'edges'
    return result


def construct_cytoscape_node_data(node, type="value", level=0):
    result =  {"data": {"id": node, "type": "value", "level": level}}
    if level == 0:
        return result
    else:
        result['group'] = 'nodes'
        return result


def networkx_to_cytoscape(edges, entity_list=[], api_list=[], endpoint_list=[]):
    elements = []
    unique_nodes = []
    for _edge in edges:
        for _node in _edge:
            if _node not in unique_nodes:
                unique_nodes.append(_node)
                elements.append(construct_cytoscape_node(_node, entity_list=entity_list, api_list=api_list, endpoint_list=endpoint_list))
        elements.append(construct_cytoscape_edge(_edge))
    return elements



class ConnectingPathHandler(BaseHandler):
    def post(self):
        start = self.get_argument('start')
        end = self.get_argument('end')
        max_api = self.get_argument('max_api')
        print(start)
        paths = bt_explorer.find_path(start, end, max_no_api_used=int(max_api), dictformat=False, display_graph=False)
        edges = []
        for _edge in bt_explorer.temp_G.edges():
            edges.append((_edge[0], _edge[1], find_edge_label(bt_explorer.temp_G, _edge[0], _edge[1])))
        no_duplicate = [_item['preferred_name'] for _item in list(bt_explorer.registry.bioentity_info.values())] + list(bt_explorer.registry.endpoint_info.keys())
        plotly_results = networkx_to_plotly(edges, duplicates_not_allowed=no_duplicate)
        self.write(json.dumps({"plotly": plotly_results, "paths": paths}))


class ConnectingInputHandler(BaseHandler):
    def post(self):
        _input = self.get_argument('input')
        print(_input)
        edges = []
        endpoints = bt_explorer.api_map.successors(_input)
        if endpoints:
            for _endpoint in endpoints:
                edges.append((_input, _endpoint, find_edge_label(bt_explorer.api_map, _input, _endpoint)))
                outputs = bt_explorer.api_map.successors(_endpoint)
                if outputs:
                    edges.extend([(_endpoint, _output, find_edge_label(bt_explorer.api_map, _endpoint, _output)) for _output in outputs])
        plotly_results = networkx_to_plotly(edges, duplicates_not_allowed=bt_explorer.registry.endpoint_info.keys())
        self.write(json.dumps({"plotly": plotly_results}))

class Input2EndpointHandler(BaseHandler):
    """
    Return endpoints which accepts given input
    """
    def post(self):
        _input = self.get_argument('input')
        endpoints = list(bt_explorer.api_map.successors(_input))
        self.write(json.dumps({"endpoints": endpoints, "input": _input}))

class Endpoint2OutputHandler(BaseHandler):
    """
    Return
    ======
    Outputs which can be returned by the given endpoint
    """
    def post(self):
        _endpoint = self.get_argument('endpoint')
        outputs = list(bt_explorer.api_map.successors(_endpoint))
        self.write(json.dumps({"endpoint": _endpoint, "output": outputs}))

class ConnectingOutputHandler(BaseHandler):
    def post(self):
        _output = self.get_argument('output')
        edges = []
        endpoints = bt_explorer.api_map.predecessors(_output)
        if endpoints:
            for _endpoint in endpoints:
                edges.append((_endpoint, _output, find_edge_label(bt_explorer.api_map, _endpoint, _output)))
                inputs = bt_explorer.api_map.predecessors(_endpoint)
                inputs = [_input for _input in inputs if bt_explorer.api_map.node[_input]['type'] == 'bioentity']
                if inputs:
                    edges.extend([(_input, _endpoint, find_edge_label(bt_explorer.api_map, _input, _endpoint)) for _input in inputs])
        plotly_results = networkx_to_plotly(edges, duplicates_not_allowed=bt_explorer.registry.endpoint_info.keys())
        self.write(json.dumps({"plotly": plotly_results}))

class ApiMapHandler(BaseHandler):
    def get(self):
        bio_entity_list = [_item['preferred_name'] for _item in list(bt_explorer.registry.bioentity_info.values())]
        api_list = bt_explorer.registry.api_info.keys()
        endpoint_list = bt_explorer.registry.endpoint_info.keys()
        cytoscape_results = networkx_to_cytoscape(bt_explorer.api_map.edges(), bio_entity_list, api_list, endpoint_list)
        self.write(json.dumps(cytoscape_results))

class ApiMapHandlerSankey(BaseHandler):
    def get(self):
        plotly_results = networkx_to_plotly(bt_explorer.api_map.edges(), [_item['preferred_name'] for _item in list(bt_explorer.registry.bioentity_info.values())])
        self.write(json.dumps({"plotly": plotly_results}))

class EndpointHandler(BaseHandler):
    def post(self):
        endpoint_name = self.get_argument('endpoint')
        edges = []
        outputs = bt_explorer.api_map.successors(endpoint_name)
        edges.extend([(endpoint_name, _output, find_edge_label(bt_explorer.api_map, endpoint_name, _output)) for _output in outputs])
        inputs = bt_explorer.api_map.predecessors(endpoint_name)
        inputs = [_input for _input in inputs if bt_explorer.api_map.node[_input]['type'] == 'bioentity']
        edges.extend([(_input, endpoint_name, find_edge_label(bt_explorer.api_map, _input, endpoint_name)) for _input in inputs])
        plotly_results = networkx_to_plotly(edges, duplicates_not_allowed=bt_explorer.registry.endpoint_info.keys())
        self.write(json.dumps({"plotly": plotly_results}))

class MetaDataHandler(BaseHandler):
    def get(self, type):
        if type == 'api':
            self.write(json.dumps({'api': list(bt_explorer.registry.api_info.keys())}))
        elif type == 'endpoint':
            self.write(json.dumps({'endpoint': list(bt_explorer.registry.endpoint_info.keys())}))
        elif type == 'bioentity':
            # group all bioentity ids together based on their semantic type
            bioentity_dict = defaultdict(list)
            for _item in bt_explorer.registry.bioentity_info.values():
                bioentity_dict[_item['semantic type']].append(_item['preferred_name'])
            for k,v in bioentity_dict.items():
                bioentity_dict[k] = sorted(v)
            self.write(json.dumps({'bioentity': bioentity_dict}))
        elif type == 'bioentity_input':
            bio_entity_list = [_item['preferred_name'] for _item in list(bt_explorer.registry.bioentity_info.values())]
            inputs = [_edge[0] for _edge in bt_explorer.api_map.edges()]
            bioentity_inputs = [_entity for _entity in bio_entity_list if _entity in inputs]
            self.write(json.dumps({'input': bioentity_inputs}))

###########################################################################
# Sample Input: {path=["hgnc.symbol", 
#                      "http://mygene.info/v1/query", 
#                      "ncbigen"]
#                input = ["CDK7", "CXCR4"]}
# Sample Output: cytoscape.js format
#                [{"data": {"id": "hgnc.symbol:CKD7"}}.
#                 {"data": {"id": "hgnc.symbol:CXCR4"}},
#                 {"data": {"id": "ncbigene:1022"}},
#                 {"data": {"target": "ncbigene:1022", 
#                           "source": "hgnc.symbol:CDK7"}}]
###########################################################################    
class FindOutputHandler(BaseHandler):
    def post(self):
        path = json.loads(self.get_argument('path'))
        input_prefix, _, output_prefix = path
        # the input field by default is a list(even if it only contains one item)
        _input = json.loads(self.get_argument('input'))
        # consider adding a level parameter here
        level = int(self.get_argument('level'))
        transformed_path = bt_explorer.path_conversion(path)
        #start_point = [path[0] + ':' + _item for _item in _input]
        G_output = bt_explorer.find_output(transformed_path, _input, display_graph=False)
        nodes = G_output.nodes()
        outputs = [_node.split(':')[1] for _node in nodes if _node.startswith(output_prefix)]
        cytoscape_results = []
        for _node in nodes:
            if _node.startswith(input_prefix + ':'):
                cytoscape_results.append(construct_cytoscape_node_data(_node, level=level))
            elif _node.startswith(output_prefix + ':'):
                cytoscape_results.append(construct_cytoscape_node_data(_node, level=level+1))
            else:
                cytoscape_results.append(construct_cytoscape_node_data(_node, level=level+1))
                print('this node could not be related to either input or output:{}')
        for _edge in G_output.edges():
            cytoscape_results.append(construct_cytoscape_edge(_edge, find_edge_label(G_output, _edge[0], _edge[1]), level))
        self.write(json.dumps({'output': outputs, 'cytoscape':cytoscape_results}))


class FindEdgeLabel(BaseHandler):
    """
    This function serves as one BioThings Explorer API endpoint
    Given an endpoint and its output, return the relationship info from JSON-LD context

    Params
    ======
    endpoint: endpoint name
    output: output of the endpoint

    """
    def post(self):
        endpoint_name = self.get_argument('endpoint')
        output = self.get_argument('output')
        self.write(json.dumps({'relation': find_edge_label(bt_explorer.api_map, endpoint_name, output)}))


