import json
from collections import defaultdict
from tornado.escape import json_encode

from .basehandler import BaseHandler
from .utils import HandlerUtils

HU = HandlerUtils()
KNOWLEDGE_MAP = HU.construct_knowledge_map()

class ConnectingInputHandler(BaseHandler):
    """
    Given an API input, ConnectingInputHandler will find all APIs which
    can take the input as well as the outputs of these APIs
    """
    def get(self):
        _input = self.get_query_argument('input')
        print(_input)
        output_format = self.get_query_argument('format', None)
        edges = []
        try:
            endpoints = HU.bt_explorer.api_map.successors(_input)
            endpoints = list(endpoints)
        except:
            endpoints = None
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "The input '" + _input + "' you give is not in BioThings Explorer."}))
            return
        if endpoints:
            for _endpoint in endpoints:
                edges.append((_input, _endpoint, HU.find_edge_label(HU.bt_explorer.api_map, _input, _endpoint)))
                outputs = HU.bt_explorer.api_map.successors(_endpoint)
                if outputs:
                    edges.extend([(_endpoint, _output,
                                   HU.find_edge_label(HU.bt_explorer.api_map,
                                                                  _endpoint, _output)) for _output in outputs])
            plotly_results = HU.networkx_to_plotly(edges,
                                                   duplicates_not_allowed=HU.bt_explorer.registry.endpoint_info.keys())
            if output_format == 'plotly':
                self.write(json.dumps({"plotly": plotly_results}))
            else:
                self.write(json.dumps({"endpoints": endpoints, "input": _input}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "Could not find any APIs in BioThings Explorer which can take the input '" + _input + "'.\n Please try other inputs!"}))
            self.finish()

class EndpointHandler(BaseHandler):
    """
    Given an API endpoint, EndpointHandler will find the inputs
    as well as the outputs of the API endpoint
    """
    def get(self):
        endpoint_name = self.get_query_argument('endpoint')
        output_format = self.get_query_argument('format', None)
        if endpoint_name not in HU.bt_explorer.registry.endpoint_info:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "The API Endpoint you give is not in BioThings Explorer."}))
            return
        else:
            edges = []
            outputs = list(HU.bt_explorer.api_map.successors(endpoint_name))
            edges.extend([(endpoint_name, _output,
                           HU.find_edge_label(HU.bt_explorer.api_map, endpoint_name, _output)) for _output in outputs])
            inputs = list(HU.bt_explorer.api_map.predecessors(endpoint_name))
            inputs = [_input for _input in inputs if HU.bt_explorer.api_map.node[_input]['type'] == 'bioentity']
            edges.extend([(_input, endpoint_name,
                           HU.find_edge_label(HU.bt_explorer.api_map, _input, endpoint_name)) for _input in inputs])
            if output_format == 'plotly':
                plotly_results = HU.networkx_to_plotly(edges, duplicates_not_allowed=HU.bt_explorer.registry.endpoint_info.keys())
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
            endpoints = list(HU.bt_explorer.api_map.predecessors(_output))
        except:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "The output '" + _output + "' you give is not in BioThings Explorer."}))
            return
        if endpoints:
            for _endpoint in endpoints:
                edges.append((_endpoint, _output, HU.find_edge_label(HU.bt_explorer.api_map, _endpoint, _output)))
                inputs = HU.bt_explorer.api_map.predecessors(_endpoint)
                inputs = [_input for _input in inputs if HU.bt_explorer.api_map.node[_input]['type'] == 'bioentity']
                if inputs:
                    edges.extend([(_input, _endpoint,
                                   HU.find_edge_label(HU.bt_explorer.api_map, _input, _endpoint)) for _input in inputs])
            if output_format == 'plotly':
                plotly_results = HU.networkx_to_plotly(edges, duplicates_not_allowed=HU.bt_explorer.registry.endpoint_info.keys())
                self.write(json.dumps({"plotly": plotly_results}))
            else:
                self.write(json.dumps({"endpoints": endpoints, "output": _output}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "Could not find any APIs in BioThings Explorer which can produce the output '" + _output + "'.\n Please try other outputs!"}))
            self.finish()

class ConnectingSemanticTypesHandler(BaseHandler):
    def get(self):
        input_semantic_type = self.get_query_argument('input')
        output_semantic_type = self.get_query_argument('output')
        output_format = self.get_query_argument('format', None)
        temp_output = KNOWLEDGE_MAP
        if input_semantic_type in [_association['subject']['semantic_type'] for _association in KNOWLEDGE_MAP]:
            temp_output = [_association for _association in temp_output if _association['subject']['semantic_type'] == input_semantic_type]
        else:
            temp_output = []
            self.set_status(400)
            self.write(json.dumps({"status": 400, "error message": "The input semantic type '" + input_semantic_type + "' is not in BioThings Explorer."}))
            return
        if output_semantic_type in [_association['object']['semantic_type'] for _association in KNOWLEDGE_MAP]:
            temp_output = [_association for _association in temp_output if _association['object']['semantic_type'] == output_semantic_type]
        else:
            temp_output = []
            self.set_status(400)
            self.write(json.dumps({"status": 400, "error message": "The output semantic type '" + output_semantic_type + "' you input is not in BioThings Explorer."}))
            return
        if temp_output:
            edges = []
            for _pair in temp_output:
                edges.append((_pair['subject']['prefix'], _pair['endpoint'], 'has_input'))
                edges.append((_pair['endpoint'], _pair['object']['prefix'], _pair['predicate']))
            if output_format == 'plotly':
                plotly_results = HU.networkx_to_plotly(edges, duplicates_not_allowed=HU.bt_explorer.registry.endpoint_info.keys())
                self.write(json.dumps({"plotly": plotly_results}))
            else:
                self.write(json.dumps({"associations": temp_output}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "No path could be found connecting from '" + input_semantic_type + "' to '" + output_semantic_type + "'!\n Please try other input and output!"}))
            self.finish()

class Input2EndpointHandler(BaseHandler):
    """
    Return endpoints which accepts given input
    """
    def get(self):
        _input = self.get_query_argument('input')
        try:
            endpoints = list(HU.bt_explorer.api_map.successors(_input))
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
        outputs = list(HU.bt_explorer.api_map.successors(_endpoint))
        self.write(json.dumps({"endpoint": _endpoint, "output": outputs}))

class MetaDataHandler(BaseHandler):
    def get(self, type):
        if type == 'apis':
            self.write(json.dumps({'api': sorted(list(HU.bt_explorer.registry.api_info.keys()))}))
        elif type == 'endpoints':
            self.write(json.dumps({'endpoint': sorted(list(HU.bt_explorer.registry.endpoint_info.keys()))}))
        elif type == 'bioentities':
            # group all bioentity ids together based on their semantic type
            bioentity_dict = defaultdict(list)
            for _item in HU.bt_explorer.registry.bioentity_info.values():
                bioentity_dict[_item['semantic type']].append(_item['prefix'])
            for k, v in bioentity_dict.items():
                bioentity_dict[k] = sorted(v)
            self.write(json_encode({'bioentity': bioentity_dict}))
        elif type == 'semantic_types':
            self.write(json_encode({'semantic_types': list(set([_item['semantic type'] for _item in HU.bt_explorer.registry.bioentity_info.values()]))}))
        elif type == 'bioentity_input':
            bio_entity_list = [_item['prefix'] for _item in list(HU.bt_explorer.registry.bioentity_info.values())]
            inputs = [_edge[0] for _edge in HU.bt_explorer.api_map.edges()]
            bioentity_inputs = [_entity for _entity in bio_entity_list if _entity in inputs]
            self.write(json.dumps({'input': bioentity_inputs}))
        elif type == 'crawler_input':
            bio_entity_list = [_item['prefix'] for _item in list(HU.bt_explorer.registry.bioentity_info.values()) if _item['attribute type'] == 'ID']
            inputs = [_edge[0] for _edge in HU.bt_explorer.api_map.edges()]
            bioentity_inputs = [_entity for _entity in bio_entity_list if _entity in inputs]
            self.write(json.dumps({'input': bioentity_inputs}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "This is not a valid request!"}))
            return

class KnowledgeMap(BaseHandler):
    """
    Return subject, object, predicate information
    Users could also query based on subject, object and predicate

    Parmas
    ======
    endpoint: specify a specific endpoint name, and return all subject, object
              predicate information specific to this endpoint
    predicate: specify a specific predicate, and return all subject, object
              predicate information which contains the specified predicate
    subject.prefix: specify a specific subject prefix, and return all subject, object
              predicate information which contains the specified subject prefix
    subject.semantic_type: specify a specific subject semantic type, and return all subject, object
              predicate information which contains the specified subject semantic type
    object.prefix: specify a specific object prefix, and return all subject, object
              predicate information which contains the specified object prefix
    object.semantic_type: specify a specific object semantic type, and return all subject, object
              predicate information which contains the specified object semantic type
    """
    def get(self):
        # get parameters
        input_endpoint = self.get_query_argument('endpoint', None)
        input_predicate = self.get_query_argument('predicate', None)
        input_subject_prefix = self.get_query_argument('subject.prefix', None)
        input_object_prefix = self.get_query_argument('object.prefix', None)
        input_subject_type = self.get_query_argument('subject.semantic_type', None)
        input_object_type = self.get_query_argument('object.semantic_type', None)
        # load all association information into KNOWLEDGE_MAP
        temp_output = KNOWLEDGE_MAP
        END_OUTPUT = False
        # check if user want to filter for a specific field or combination of fields
        if input_endpoint:
            # check whether user input is valid
            if input_endpoint in HU.bt_explorer.registry.endpoint_info:
                temp_output = [_association for _association in temp_output if _association['endpoint'] == input_endpoint]
            else:
                temp_output = []
                self.set_status(400)
                self.write(json.dumps({"status": 400, "error message": "The endpoint '" + input_endpoint + "' you input is not in BioThings Explorer. \
                                      Please refer to 'http://biothings.io/explorer/api/v1/metadata/endpoints' for all endpoints currently integrated!"}))
                return
        if input_predicate and not END_OUTPUT:
            if input_predicate in [_association['predicate'] for _association in KNOWLEDGE_MAP]:
                temp_output = [_association for _association in temp_output if _association['predicate'] == input_predicate]
            else:
                temp_output = []
                self.set_status(400)
                self.write(json.dumps({"status": 400, "error message": "The predicate '" + input_predicate + "' you input is not in BioThings Explorer."}))
                return
        if input_subject_prefix and not END_OUTPUT:
            if input_subject_prefix in [_association['subject']['prefix'] for _association in KNOWLEDGE_MAP]:
                temp_output = [_association for _association in temp_output if _association['subject']['prefix'] == input_subject_prefix]
            else:
                temp_output = []
                self.set_status(400)
                self.write(json.dumps({"status": 400, "error message": "The subject prefix '" + input_subject_prefix + "' you input is not in BioThings Explorer."}))
                return
        if input_subject_type and not END_OUTPUT:
            if input_subject_type in [_association['subject']['semantic_type'] for _association in KNOWLEDGE_MAP]:
                temp_output = [_association for _association in temp_output if _association['subject']['semantic_type'] == input_subject_type]
            else:
                temp_output = []
                self.set_status(400)
                self.write(json.dumps({"status": 400, "error message": "The subject semantic type '" + input_subject_type + "' you input is not in BioThings Explorer."}))
                return
        if input_object_prefix and not END_OUTPUT:
            if input_object_prefix in [_association['object']['prefix'] for _association in KNOWLEDGE_MAP]:
                temp_output = [_association for _association in temp_output if _association['object']['prefix'] == input_object_prefix]
            else:
                temp_output = []
                self.set_status(400)
                self.write(json.dumps({"status": 400, "error message": "The object prefix '" + input_object_prefix + "' you input is not in BioThings Explorer."}))
                return
        if input_object_type and not END_OUTPUT:
            if input_object_type in [_association['object']['semantic_type'] for _association in KNOWLEDGE_MAP]:
                temp_output = [_association for _association in temp_output if _association['object']['semantic_type'] == input_object_type]
            else:
                temp_output = []
                self.set_status(400)
                self.write(json.dumps({"status": 400, "error message": "The object semantic type '" + input_object_type + "' you input is not in BioThings Explorer."}))
                return
        # output
        if temp_output:
            self.write(json.dumps({"associations": temp_output}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "error message": "No associations could be found for the input you give!!"}))
