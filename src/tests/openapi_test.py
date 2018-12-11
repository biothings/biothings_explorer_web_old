import os, sys
from os import path

lib_path = os.path.abspath(os.path.join('..', 'biothings_explorer'))
sys.path.append( path.dirname( path.dirname( path.abspath(lib_path))))

from biothings_explorer import BioThingsExplorer
from biothings_explorer.utils import int2str
from biothings_explorer.utils import readFile
from .input_output import input_output_dict
import requests

bt_explorer = BioThingsExplorer()

import unittest

def find_uri_from_jsonld(d, uris=[]):
    """
    Iterative function
    Given a JSON-LD context file as Python Dictionary,
    return all bio-entity URIs in that context file
    together with the relationship(s) as a set
    e.g. {'http://identifiers.org/pdb/': {'ont:has3DStructure'}}

    Params
    ======
    d: (dict)
        JSON-LD context
    relation: (dict)
        temporarily store relation info
    """
    for k, v in d.items():
        if isinstance(v, dict) and "@context" in v and "@base" in v["@context"]:
            uris.append(v["@context"]["@base"])
        # if v is a dict and doesnt have @base, then reiterative the process
        elif isinstance(v, dict):
            find_uri_from_jsonld(v, uris=uris)
        elif isinstance(v, str) and v.startswith('http'):
            uris.append(v)
    return uris

class TestOpenAPI(unittest.TestCase):
    """
    Test whether OpenAPI files for each API could be fed
    by BioThings Explorer
    Test items include:
    1) All input/output URIs are documented in ID_Mapping file
    2) Given input, whether API calls could be generated
    3) Whether JSON-LD context files are valid by extracting output
    """

    def test_openapi_make_call(self):
        # loop through each endpoint
        #for _endpoint in bt_explorer.registry.endpoint_info.keys():
        for _endpoint in input_output_dict.keys():
            print('Current processing {}'.format(_endpoint))
            # check whether endpoint is included in input_output_dict
            self.assertIn(_endpoint, input_output_dict, 'This API is not in input_output_dict: ' + _endpoint)
            if _endpoint in input_output_dict:
                for _test in input_output_dict[_endpoint]:
                    print('Input for test {}'.format(str(_test['input'])))
                    self.assertIn('input', _test, 'Sample input is not specified in the input_output file for this endpoint: ' + _endpoint)
                    self.assertIn('output', _test, 'Sample output is not specified in the input_output file for this endpoint: ' + _endpoint)
                    api_call_params = bt_explorer.apiCallHandler.call_api(_test['input'], _endpoint)
                    response = requests.get(api_call_params[0], params=api_call_params[1], headers={'Accept': 'application/json'})
                    self.assertEqual(response.status_code, 200, "The API call for " + str(api_call_params) + " doesn't return response 200, it returns: " + str(response.status_code))
                    data = response.json()
                    int2str(data)
                    self.assertIsInstance(data, dict, "The output of the API call is not a dictionary" + _endpoint)
                    for _output_uri in _test["output"].keys():
                        outputs_list = bt_explorer.apiCallHandler.extract_output([data], _endpoint, _output_uri, predicate=None)
                        self.assertIsNotNone(outputs_list[0], "Nothing could be extracted for the output_uri specified: " + _output_uri)
                        outputs = [_item[0] for _item in outputs_list[0][0]]
                        self.assertIn(_test["output"][_output_uri], set(outputs))
                    print('Passed!!')
            print('Passed all validations!!!')
            print('#########################################################################################################')
        print('All OpenAPI specs have been tested and validated!!')

    def test_whether_all_input_output_uri_are_documented_in_id_mapping_file(self):
        # loop through each API listed in API_list.yml
        print('Start to Test Consistency between OpenAPI specs and ID_MAPPING FILE NOW!!!')
        for _api in bt_explorer.registry.openapi_spec_path_list:
            print('Running test on {}'.format(_api.split('/')[-2]))
            data = readFile(_api)
            self.assertIsNotNone(data, 'The OpenAPI specs from the following file ' + _api + ' is empty!')
            for _name, _info in data['paths'].items():
                # there are cases where x-responseValueType is not included in the Path
                if 'x-responseValueType' in _info['get']['responses']['200']:
                    output_list = [_item['valueType'] for _item in _info['get']['responses']['200']['x-responseValueType']]
                    for _output in output_list:
                        self.assertIn(_output, bt_explorer.registry.bioentity_info)
                # there are cases where x-valueType is not included in the Path
                if 'x-valueType' in _info['get']['parameters'][0]:
                    input_list = [_item for _item in _info['get']['parameters'][0]['x-valueType']]
                    for _input in input_list:
                        self.assertIn(_input, bt_explorer.registry.bioentity_info)
            print("Passed!")

    def test_whether_x_valueType_and_x_requestTemplate_are_consistent(self):
        # loop through each API listed in API_list.yml
        print('Start to Test Consistency inside OpenAPI specs!!!')
        for _api in bt_explorer.registry.openapi_spec_path_list:
            print('Running test on {}'.format(_api.split('/')[-2]))
            # fetch the openAPI file
            data = readFile(_api)
            # check whether the file is empty
            self.assertIsNotNone(data, 'The OpenAPI specs from the following file ' + _api + ' is empty!')
            # loop through each endpoint in the API specs
            for _name, _info in data['paths'].items():
                # check if it contains 'x-valueType' information
                if 'x-valueType' in _info['get']['parameters'][0]:
                    # check if x-valuetype and x-requesttemplate matches
                    valuetype_list = [_item for _item in _info['get']['parameters'][0]['x-valueType']]
                    requesttemplate_list = [_item['valueType'] for _item in _info['get']['parameters'][0]['x-requestTemplate']]
                    self.assertEqual(set(valuetype_list), set(requesttemplate_list))
            print("Passed!")

    def test_whether_openapi_and_jsonld_context_are_consistent(self):
        # loop through each API listed in API_list.yml
        print('Start to Test Consistency inside OpenAPI specs!!!')
        for _api in bt_explorer.registry.openapi_spec_path_list:
            print('Running test on {}'.format(_api.split('/')[-2]))
            # fetch the openAPI file
            data = readFile(_api)
            # check whether the file is empty
            self.assertIsNotNone(data, 'The OpenAPI specs from the following file ' + _api + ' is empty!')
            # loop through each endpoint in the API specs
            for _name, _info in data['paths'].items():
                # check if 'x-reponseValueType' exists
                if 'x-responseValueType' in _info['get']['responses']['200']:
                    # get all URIs representing API outputs
                    output_list = [_item['valueType'] for _item in _info['get']['responses']['200']['x-responseValueType']]
                # check whether jsonld context file exists for this endpoint
                if 'x-JSONLDContext' in _info['get']['responses']['200']:
                    jsonld_path = os.path.join(bt_explorer.registry.registry_path, _info['get']['responses']['200']['x-JSONLDContext'])
                    jsonld_context_file = readFile(jsonld_path)
                    self.assertIsNotNone(jsonld_context_file, 'The JSON-LD from the following file ' + jsonld_path + ' is empty!')
                    jsonld_uri_list = find_uri_from_jsonld(jsonld_context_file)
                self.assertEqual(len(list(set(output_list)-set(jsonld_uri_list))), 0, 'The output URIs are not all documented in the JSONLD context file for this endpoint: ' + _name)
            print('Passed!')

    def check_whether_there_are_redundant_uris_in_ID_Mapping_file(self):
        openapi_uri_list = []
        for _api in bt_explorer.registry.openapi_spec_path_list:
            data = readFile(_api)
            self.assertIsNotNone(data, 'The OpenAPI specs from the following file ' + _api + ' is empty!')
            for _name, _info in data['paths'].items():
                # there are cases where x-responseValueType is not included in the Path
                if 'x-responseValueType' in _info['get']['responses']['200']:
                    output_list = [_item['valueType'] for _item in _info['get']['responses']['200']['x-responseValueType']]
                    openapi_uri_list += output_list
                # there are cases where x-valueType is not included in the Path
                if 'x-valueType' in _info['get']['parameters'][0]:
                    input_list = [_item for _item in _info['get']['parameters'][0]['x-valueType']]
                    openapi_uri_list += input_list
        print("All URIs have been fetched from OpenAPI specs!")
        self.assertEqual(set(openapi_uri_list), set(bt_explorer.registry.bioentity_info.keys()))
        print("No redundant URIs have been found in the ID Mapping File!")


if __name__ == '__main__':
    unittest.main()