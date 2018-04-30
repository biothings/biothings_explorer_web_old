import json
import requests
import grequests
import time

from .api_registry_parser import RegistryParser
from .jsonld_processor import JSONLDHelper
from .output_organizer import OutputOrganizor
from .networkx_helper import NetworkxHelper
from .utils import int2str

class ApiCallHandler:
    def __init__(self):
        """
        Handles API calls, including:
        1) Find the right API given input/output type
        2) Preprocessing Input
        3) Make API calls based on given input
        4) Extract Output from API call results
        """
        self.registry = RegistryParser(readmethod='filepath', initialize=True)
        self.jh = JSONLDHelper()
        self.oo = OutputOrganizor()
        self.nh = NetworkxHelper()

    def check_if_exists_multiple_params(self, endpoint_name):
        """
        Some API endpoints takes more than one required input
        e.g. humanbase API ('http://hb.flatironinstitute.org/api') specifies 'tissue'
        and 'geneid' as two required input parameters
        Thus, this function checks whether there exists multiple required parameters
        It returns True when there exists >1 parameters, False if only 1 parameter is required

        Params
        ======
        endpoint_name: (str)
            The endpoint name to check
        """
        required_paras = sum([1 for _para in self.registry.endpoint_info[endpoint_name]['get']['parameters'] if _para['required']])
        if required_paras > 1:
            return True
        else:
            return False

    def api_endpoint_locator(self, _input, _output):
        """
        This function fullfill task 1 of the class ApiCallHandler
        Given an input/output pair, return the endpoint(s) which could do the transformation

        Params
        ======
        input: (str)
            In the form of URI. Should be part of an endpoint's x-valueType
        output: (str)
            In the form of URI. Should be part of an endpoint's x-responeType

        """
        endpoint_list = []
        # loop through each API endpoint, compare its input/output with the input/output given by the user
        # if hits, append to the list
        for _endpoint, _info in self.registry.endpoint_info.items():
            if _input in _info['input'] and _output in _info['output']:
                endpoint_list.append(_endpoint)
        # check if endpoint is found
        if not endpoint_list:
            print('Could not find an API endpoint which takes the desired input: {} and return the desired output: {}'.format(_input, _output))
        return endpoint_list

    def preprocessing_input(self, value, endpoint_name):
        '''
        Based on endpoint info, handle the input given
        1) If the parameter type for the endpoint is 'array', treat the whole input as a list
        2) If the parameter is string, treat each item individually

        params
        ======
        value: (str or list)
            input_value for endpoint
        endpoint_name: (str)
            The endpoint to make api call

        '''
        # if the endpoint takes array as input, turn input value into [list]
        if self.registry.endpoint_info[endpoint_name]['get']['parameters'][0]['schema']['type'] == 'array':
            if type(value) == list:
                return [value]
            else:
                print("Wrong input type error: {} takes list as input, while {} type input is given by the user".format(endpoint_name, type(value)))
        # if the endpoint takes string as input, turn input value into [string1, string2, string3]
        else:
            if type(value) == list:
                return value
            else:
                return [value]

    def call_api(self, uri_value_dict, endpoint_name):
        """
        make api calls
        1) If the input_type is in endpoint path, then replace the input_type name in endpoint with the input value
        2) If the input_type is in query
           a) If there exists a requestTemplate, then follow the template to constrcut api call
           b) If no template, construct a new {para: value} pair

        TODO: currently this function only handles 'get' method
              Later on, we should extend it to handle 'post' method for batch queries

        params
        ======
        uri_value_dict: (dict)
            Dictionary with URI representing the input type as key, and input value as value
        endpoint_name: (str)
            The endpoint to make api call

        """
        if type(uri_value_dict) != dict:
            print('The parameter uri_value_dict should be of type dict!! Your input is of type {}!'.format(type(uri_value_dict)))
            return
        if endpoint_name not in self.registry.endpoint_info:
            print('The endpoint you specify ({}) is not in the registry'.format(endpoint_name))
            return
        results = {}
        method = 'get'
        for _para in self.registry.endpoint_info[endpoint_name][method]['parameters']:
            # handle cases where input value is part of the url
            if _para['in'] == 'path':
                for _input_type in _para['x-valueType']:
                    if _input_type in uri_value_dict:
                        for _template in _para['x-requestTemplate']:
                            if _template['valueType'] == _input_type:
                                if _template['template'] in endpoint_name:
                                    endpoint_name = endpoint_name.replace('{' + _para['name'] + '}', str(uri_value_dict[_input_type]))
                                else:
                                    endpoint_name = self.registry.endpoint_info[endpoint_name]['api'] + _template['template'].replace('{' + _para['name'] + '}', str(uri_value_dict[_input_type]))
            # handle cases for query
            else:
                # check whether the parameter is required
                if _para['required']:
                    # if the para has a request template, then put value into the placeholder 'input_value'
                    if 'x-requestTemplate' in _para:
                        for _template in _para['x-requestTemplate']:
                            if _template['valueType'] == 'default':
                                results[_para['name']] = _template['template'].replace('input_value', json.dumps(list(uri_value_dict.values())[0]))
                            elif _template['valueType'] in uri_value_dict.keys():
                                results[_para['name']] = _template['template'].replace('input_value', uri_value_dict[_template['valueType']])
                    else:
                        results[_para['name']] = list(uri_value_dict.values())[0]
        """
        # switch to grquests to handle multiple API calls together
        if requests.get(endpoint_name, params=results).status_code == 200:
            return requests.get(endpoint_name, params=results)
        else:
            print('This API call returns no results. The URI given is {}, the endpoint given is {}'.format(uri_value_dict, endpoint_name))
            return
        """
        return (endpoint_name, results)

    def preprocess_json_doc(self, json_doc, endpoint_name):
        """
        Preprocessing json doc, including following steps:
        1) Convert all integers in the json_doc into string

        """
        if type(json_doc) == list:
            json_doc = {'data': json_doc}
        int2str(json_doc)
        return json_doc

    def extract_output(self, json_doc, endpoint_name, output_uri, predicate):
        """
        extract output from json_doc
        1) determine the output type
        2) If output_type is entity, use jsonld to extract the output
        3) if output_type is object, use the path from openapi to extract the output

        params
        ======
        json_doc: (dict)
            preprocessed json_doc to extract output
        endpoint_name: (str)
            used to find path
        output_uri: (str)
            the output type to extract
        predicate: (str)
            the relationship between input and output

        """
        # get the output_type of the output, could be 'entity' or 'object'
        if output_uri in self.registry.bioentity_info:
            output_type = self.registry.bioentity_info[output_uri]['semantic type']
        else:
            print("The output_uri specified {} could not be found in the registry!".format(output_uri))
            return
        # if output_type is entity, use JSON-LD to extract the output
        jsonld_context = self.registry.endpoint_info[endpoint_name]['jsonld_context']
        nquads = self.jh.json2nquads(json_doc, jsonld_context)
        properties = self.jh.fetch_properties_by_association_and_prefix_in_nquads(nquads, predicate, output_uri)
        properties = [self.oo.nquads2dict(_property) for _property in properties]
        results = []
        for _property in properties:
            if _property:
                results.append((_property, self.registry.bioentity_info[output_uri]['preferred_name']))
            else:
                results.append(None)
        return results


    def input2output(self, input_type, input_value, endpoint_name, output_type, predicate=None, additional_parameters={}, _type='prefix'):
        """
        This is the main function of the class
        Given input, endpoint, output, etc, perform the following steps:
        1) Preprocess input based on endpoint type
        2) Make API calls
        3) Preprocess the JSON doc from step 2
        4) Extract the output based on output_type and predicate
        """
        if _type == 'prefix':
            input_type = self.registry.prefix2uri(input_type)
            output_type = self.registry.prefix2uri(output_type)
        if not predicate:
            predicate = self.nh.find_edge_label(endpoint_name, self.registry.bioentity_info[output_type]['preferred_name'])
            if type(predicate) != list:
                predicate = predicate.replace('assoc:', 'http://biothings.io/explorer/vocab/objects/')
            else:
                predicate = [_predicate.replace('assoc:', 'http://biothings.io/explorer/vocab/objects/') for _predicate in predicate]
        final_results = []
        # preprocess the input
        processed_input = self.preprocessing_input(input_value, endpoint_name)
        # retrieve json doc
        api_call_params = []
        for _input_value in processed_input:
            uri_value = {input_type: _input_value}
            if additional_parameters:
                uri_value.update(additional_parameters)
            api_call_params.append(self.call_api(uri_value, endpoint_name))
        start = time.time()
        rs = (grequests.get(u, params=v) for (u,v) in api_call_params)
        responses = grequests.map(rs)
        if responses and responses[0].status_code == 200:
            rs = (grequests.get(u, params=v, headers={'Accept': 'application/json'}) for (u,v) in api_call_params)
            responses = grequests.map(rs)
            #api_call_response = self.call_api(uri_value, endpoint_name)
        valid_responses = [self.preprocess_json_doc(api_call_response.json(), endpoint_name) if api_call_response.status_code == 200 else {} for api_call_response in responses]
        print('Time used in making API calls: {:.2f} seconds'.format(time.time() - start))
        start = time.time()
        if type(predicate) != list:
            outputs = self.extract_output(valid_responses, endpoint_name, output_type, predicate=predicate)
            for i in range(len(outputs)):
                if outputs[i]:
                    final_results.append({'input': (processed_input[0], self.registry.bioentity_info[input_type]['preferred_name']), 'output': (outputs[i]), 'endpoint': endpoint_name, 'target': outputs[i][0]['target']['id']})
        else:
            for _predicate in predicate:
                outputs = self.extract_output(valid_responses, endpoint_name, output_type, predicate=_predicate)
            for i in range(len(outputs)):
                if outputs[i]:
                    final_results.append({'input': (processed_input[i], self.registry.bioentity_info[input_type]['preferred_name']), 'output': (outputs[i]), 'endpoint': endpoint_name, 'target': outputs[i][0]['target']['id']})
        print('Time used in organizing outputs: {:.2f} seconds'.format(time.time() - start))
        return final_results