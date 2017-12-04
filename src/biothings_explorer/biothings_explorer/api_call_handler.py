import json
import requests

from .api_registry_parser import RegistryParser
from .jsonld_processor import json2nquads
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
                endpoint_name = endpoint_name.replace('{' + _para['name'] + '}', str(uri_value_dict[_para['x-valueType'][0]]))
            # handle cases for query
            else:
                # check whether the parameter is required
                if _para['required']:
                    # if the para has a request template, then put value into the placeholder {{input}}
                    if 'x-requestTemplate' in _para:
                        for _template in _para['x-requestTemplate']:
                            if _template['valueType'] == 'default':
                                results[_para['name']] = _template['template'].replace('{{input}}', json.dumps(list(uri_value_dict.values())[0]))
                            elif _template['valueType'] in uri_value_dict.keys():
                                results[_para['name']] = _template['template'].replace('{{input}}', json.dumps(uri_value_dict[_template['valueType']]))
                    else:
                        results[_para['name']] = list(uri_value_dict.values())[0]
        if requests.get(endpoint_name, params=results).status_code == 200:
            return requests.get(endpoint_name, params=results)
        else:
            print('This API call returns no results. The URI given is {}, the endpoint given is {}'.format(uri_value_dict, endpoint_name))
            return

    def preprocess_json_doc(self, json_doc, endpoint_name):
        """
        Preprocessing json doc, including following steps:
        1) Convert all integers in the json_doc into string
        2) If the endpoint is MyVariant, convert all ":" into "-"
            because jsonld could not handle ':'

        TODO: should work with jsonld folks to support ":" as part of the value
        """
        int2str(json_doc)
        if endpoint_name.startswith('http://myvariant.info/'):
            if "_id" in json_doc:
                json_doc["_id"] = json_doc["_id"].replace(':', '-')
            elif "hits" in json_doc:
                for _doc in json_doc["hits"]:
                    if "_id" in _doc:
                        _doc['_id'] = _doc['_id'].replace(":", "-")
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
            output_type = self.registry.bioentity_info[output_uri]['type']
        else:
            print("The output_uri specified {} could not be found in the registry!".format(output_uri))
            return
        # if output_type is entity, use JSON-LD to extract the output
        if output_type == 'Entity':
            jsonld_context = self.registry.endpoint_info[endpoint_name]['jsonld_context']
            outputs = json2nquads(json_doc, jsonld_context, output_uri, predicate)
            if outputs:
                return (outputs, self.registry.bioentity_info[output_uri]['preferred_name'])
            else:
                print("No output could be found from the given json_doc and output type!")
                return
        # if output_type is object, use OpenAPI specs to extract the output
        else:
            response = self.endpoint_info[endpoint_name]['get']['responses']['200']['x-responseValueType']
            # get the dot path for extracting output
            for _response in response:
                if _response['valueType'] == output_uri:
                    output_path = _response['path']
                else:
                    print("Could not find the path to extract output in OpenAPI specs in endpoint: {}".format(endpoint_name))
                    return
            # extract output
            outputs_command = 'json_doc'
            for _item in output_path.split('.'):
                outputs_command += ('["' + _item + '"]')
            try:
                outputs = eval(outputs_command)
            except:
                print("Could not extract the output from the path given {}".format(outputs_command))
                return
            return (outputs, self.registry.bioentity_info[output_uri]['preferred_name'])

    def input2output(self, input_type, input_value, endpoint_name, output_type, predicate=None, additional_parameters={}, type='prefix'):
        """
        This is the main function of the class
        Given input, endpoint, output, etc, perform the following steps:
        1) Preprocess input based on endpoint type
        2) Make API calls
        3) Preprocess the JSON doc from step 2
        4) Extract the output based on output_type and predicate
        """
        if type == 'prefix':
            input_type = self.registry.prefix2uri(input_type)
            output_type = self.registry.prefix2uri(output_type)
        final_results = []

        # preprocess the input
        processed_input = self.preprocessing_input(input_value, endpoint_name)
        # retrieve json doc
        for _input_value in processed_input:
            uri_value = {input_type: _input_value}
            if additional_parameters:
                uri_value.update(additional_parameters)
            api_call_response = self.call_api(uri_value, endpoint_name)
            if api_call_response:
                json_doc = self.preprocess_json_doc(api_call_response.json(), endpoint_name)
            else:
                print('This API call returns no response. Endpoint name: {}, Input value type: {}. Input value: {}'
                      .format(endpoint_name, input_type, input_value))
            # extract the output based on output_type & predicate
            output_info = self.extract_output(json_doc, endpoint_name, output_type, predicate=predicate)
            if output_info:
                final_results.append({'input': (_input_value, self.registry.bioentity_info[input_type]['preferred_name']), 'output': (output_info)})
            else:
                print('The API call returns response. But no appropriate output could be extracted. Output type given is : {}. Predicate given is: {}'
                      .format(output_type, predicate))
        return final_results
