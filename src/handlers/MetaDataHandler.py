import json
from collections import defaultdict
from tornado.escape import json_encode

from .basehandler import BaseHandler
from .utils import HandlerUtils

class ConnectingInputHandler(BaseHandler):
    """
    Given an API input, ConnectingInputHandler will find all APIs which
    can take the input as well as the outputs of these APIs
    """
    def get(self):
        _input = self.get_query_argument('input')
        output_format = self.get_query_argument('format', None)
        edges = []
        try:
            endpoints = HandlerUtils().bt_explorer.api_map.successors(_input)
            endpoints = list(endpoints)
        except:
            endpoints = None
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "The input '" + _input + "' you give is not in BioThings Explorer."}))
            return
        if endpoints:
            for _endpoint in endpoints:
                edges.append((_input, _endpoint, HandlerUtils().find_edge_label(HandlerUtils().bt_explorer.api_map, _input, _endpoint)))
                outputs = HandlerUtils().bt_explorer.api_map.successors(_endpoint)
                if outputs:
                    edges.extend([(_endpoint, _output,
                                   HandlerUtils().find_edge_label(HandlerUtils().bt_explorer.api_map, _endpoint, _output)) for _output in outputs])
            plotly_results = HandlerUtils().networkx_to_plotly(edges,
                                                               duplicates_not_allowed=HandlerUtils().bt_explorer.registry.endpoint_info.keys())
            if output_format == 'plotly':
                self.write(json.dumps({"plotly": plotly_results}))
            else:
                self.write(json.dumps({"endpoints": endpoints, "input": _input}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "Could not find any APIs in BioThings Explorer which can take the input"}))
            self.finish()

class EndpointHandler(BaseHandler):
    """
    Given an API endpoint, EndpointHandler will find the inputs
    as well as the outputs of the API endpoint
    """
    def get(self):
        endpoint_name = self.get_query_argument('endpoint')
        output_format = self.get_query_argument('format', None)
        if endpoint_name not in HandlerUtils().bt_explorer.registry.endpoint_info:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "The API Endpoint you give is not in BioThings Explorer."}))
            return
        else:
            edges = []
            outputs = list(HandlerUtils().bt_explorer.api_map.successors(endpoint_name))
            edges.extend([(endpoint_name, _output,
                           HandlerUtils().find_edge_label(HandlerUtils().bt_explorer.api_map, endpoint_name, _output)) for _output in outputs])
            inputs = list(HandlerUtils().bt_explorer.api_map.predecessors(endpoint_name))
            inputs = [_input for _input in inputs if HandlerUtils().bt_explorer.api_map.node[_input]['type'] == 'bioentity']
            edges.extend([(_input, endpoint_name,
                           HandlerUtils().find_edge_label(HandlerUtils().bt_explorer.api_map, _input, endpoint_name)) for _input in inputs])
            if output_format == 'plotly':
                plotly_results = HandlerUtils().networkx_to_plotly(edges, duplicates_not_allowed=HandlerUtils().bt_explorer.registry.endpoint_info.keys())
                self.write(json.dumps({"plotly": plotly_results}))
            else:
                self.write(json.dumps({"endpoint": endpoint_name, "input": inputs, "output": outputs}))

class ConnectingOutputHandler(BaseHandler):
    """
    Given an bioentity, ConnectingOutputHandler will find the APIs which can generate
    the output as well as the inputs of the APIs
    """
    def get(self):
        _output = self.get_query_argument('output')
        output_format = self.get_query_argument('format', None)
        edges = []
        try:
            endpoints = list(HandlerUtils().bt_explorer.api_map.predecessors(_output))
        except:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "The output '" + _output + "' you give is not in BioThings Explorer."}))
            return
        if endpoints:
            for _endpoint in endpoints:
                edges.append((_endpoint, _output, HandlerUtils().find_edge_label(HandlerUtils().bt_explorer.api_map, _endpoint, _output)))
                inputs = HandlerUtils().bt_explorer.api_map.predecessors(_endpoint)
                inputs = [_input for _input in inputs if HandlerUtils().bt_explorer.api_map.node[_input]['type'] == 'bioentity']
                if inputs:
                    edges.extend([(_input, _endpoint,
                                   HandlerUtils().find_edge_label(HandlerUtils().bt_explorer.api_map, _input, _endpoint)) for _input in inputs])
            if output_format == 'plotly':
                plotly_results = HandlerUtils().networkx_to_plotly(edges, duplicates_not_allowed=HandlerUtils().bt_explorer.registry.endpoint_info.keys())
                self.write(json.dumps({"plotly": plotly_results}))
            else:
                self.write(json.dumps({"endpoints": endpoints, "output": _output}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "Could not find any APIs in BioThings Explorer which can produce the output"}))
            self.finish()

class Input2EndpointHandler(BaseHandler):
    """
    Return endpoints which accepts given input
    """
    def get(self):
        _input = self.get_query_argument('input')
        try:
            endpoints = list(HandlerUtils().bt_explorer.api_map.successors(_input))
        except:
            endpoints = None
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "could not find any APIs in BioThings Explorer which has the input"}))
            return
        if endpoints:
            self.write(json.dumps({"endpoints": endpoints, "input": _input}))

class Endpoint2OutputHandler(BaseHandler):
    """
    Return
    ======
    Outputs which can be returned by the given endpoint
    """
    def post(self):
        _endpoint = self.get_argument('endpoint')
        outputs = list(HandlerUtils().bt_explorer.api_map.successors(_endpoint))
        self.write(json.dumps({"endpoint": _endpoint, "output": outputs}))

class MetaDataHandler(BaseHandler):
    def get(self, type):
        if type == 'apis':
            self.write(json.dumps({'api': sorted(list(HandlerUtils().bt_explorer.registry.api_info.keys()))}))
        elif type == 'endpoints':
            self.write(json.dumps({'endpoint': sorted(list(HandlerUtils().bt_explorer.registry.endpoint_info.keys()))}))
        elif type == 'bioentities':
            # group all bioentity ids together based on their semantic type
            bioentity_dict = defaultdict(list)
            for _item in HandlerUtils().bt_explorer.registry.bioentity_info.values():
                bioentity_dict[_item['semantic type']].append(_item['preferred_name'])
            for k, v in bioentity_dict.items():
                bioentity_dict[k] = sorted(v)
            self.write(json_encode({'bioentity': bioentity_dict}))
        elif type == 'bioentity_input':
            bio_entity_list = [_item['preferred_name'] for _item in list(HandlerUtils().bt_explorer.registry.bioentity_info.values())]
            inputs = [_edge[0] for _edge in HandlerUtils().bt_explorer.api_map.edges()]
            bioentity_inputs = [_entity for _entity in bio_entity_list if _entity in inputs]
            self.write(json.dumps({'input': bioentity_inputs}))
