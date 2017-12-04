from urllib.parse import urljoin
import os.path
from collections import defaultdict

from .utils import readFile
from .config import FILE_PATHS
from .jsonld_processor import find_base


class RegistryParser:
    def __init__(self, readmethod, initialize=False):
        """
        Parse the openapi files and JSON-LD context files located at
        https://github.com/NCATS-Tangerine/translator-api-registry

        Params
        ======
        readmethod: (str)
            http -- read from url
            filepath -- read from local
        initialize: (boolean)
            whether to read in all files when calling the class
        """
        self.readmethod = readmethod
        self.bioentity_info = {}
        self.api_info = {}
        self.endpoint_info = {}
        self.openapi_spec_path_list = []
        if readmethod == 'http':
            self.registry_path = FILE_PATHS['registry_repo']['url']
            self.api_list_path = FILE_PATHS['api_list']['url']
            self.id_mapping_path = FILE_PATHS['id_mapping']['url']
        elif readmethod == 'filepath':
            self.registry_path = FILE_PATHS['registry_repo']['file']
            self.api_list_path = FILE_PATHS['api_list']['file']
            self.id_mapping_path = FILE_PATHS['id_mapping']['file']
        elif readmethod:
            print('Invalid readmethod {}!!!. Please choose either http or filepath'.format(readmethod))
        else:
            print('Please specify a readmethod. It could be either http or filepath!')
        if initialize:
            # read in all biological entity info
            self.bioentity_info = self.read_id_mapping_file()
            # read in api list
            self.openapi_spec_path_list = self.read_api_list_file()
            # read openapi file for each api
            for _file_path in self.openapi_spec_path_list:
                parsed_result = self.parse_openapi_file(_file_path)
                if 'api' in parsed_result:
                    self.api_info.update(parsed_result['api'])
                if 'endpoints' in parsed_result:
                    self.endpoint_info.update(parsed_result['endpoints'])

    def read_id_mapping_file(self):
        """
        read in the ID-MAPPING.csv file
        and parse it into bioentity_info dictionary
        The dictionary key is the URI, and it's value contains registry_identifier, etc.
        """
        data = readFile(self.id_mapping_path)
        # turn data frame into a dictionary and store in bioentity_info
        for index, row in data.iterrows():
            self.bioentity_info[row['URI']] = {'registry_identifier': row['Registry identifier'], 'alternative_names': row['Alternative name(s)'],
                                               'description': row['Description'], 'identifier_pattern': row['Identifier pattern'],
                                               'preferred_name': row['Recommended name'], 'type': row['Type'], 'semantic type': row['Semantic Type']}
        return self.bioentity_info

    def prefix2uri(self, prefix):
        """
        Given a bio-entity in prefix format, return its URI

        Params
        ======
        prefix: (str)
            bio-entity in prefix format

        Return
        ======
        bio-entity in its URI format
        """
        for k, v in self.bioentity_info.items():
            if v['preferred_name'] == prefix:
                return k
        # print error message if no URI was found
        print('No URI could be found for the prefix provided: {}'.format(prefix))

    def read_api_list_file(self):
        """
        read in the API_LIST.yml file
        and parse it into openapi_spec_path_list
        The list contains paths for each openapi file
        """
        api_list_file = readFile(self.api_list_path)
        if self.readmethod == 'http':
            self.openapi_spec_path_list = [urljoin(self.registry_path, _api['metadata']) for _api in api_list_file['APIs']]
            return self.openapi_spec_path_list
        elif self.readmethod == 'filepath':
            self.openapi_spec_path_list = [os.path.join(self.registry_path, _api['metadata']) for _api in api_list_file['APIs']]
            return self.openapi_spec_path_list
        else:
            return

    def parse_openapi_file(self, file_name):
        """
        read in the API openapi yaml file
        and parse it into a dictionary
        containing api and endpoint info separately

        Params
        ======
        file_name: (str)
            The path to the (individual) openapi file
        """
        data = readFile(file_name)
        if not data:
            return
        parsed_result = {'api': {}, 'endpoints': {}}
        api_name = data['info']['title']
        # parse api info
        parsed_result['api'] = {api_name: {'info': data['info'], 'servers': data['servers'], 'endpoints': []}}
        # parse endpoint info
        for _name, _info in data['paths'].items():
            endpoint_name = data['servers'][0]['url'] + _name
            parsed_result['endpoints'].update({endpoint_name: _info})
            _output = [_item['valueType'] for _item in _info['get']['responses']['200']['x-responseValueType']]
            # extract relationship info from the json-ld context file
            relation = {}
            if 'x-JSONLDContext' in _info['get']['responses']['200']:
                if self.readmethod == 'http':
                    jsonld_path = urljoin(self.registry_path, _info['get']['responses']['200']['x-JSONLDContext'])
                elif self.readmethod == 'filepath':
                    jsonld_path = os.path.join(self.registry_path, _info['get']['responses']['200']['x-JSONLDContext'])
                relation = find_base(readFile(jsonld_path), relation=defaultdict(set))
                parsed_result['endpoints'][endpoint_name].update({'jsonld_context': jsonld_path})
            for _op in _output:
                if _op not in relation:
                    relation[_op] = ['ont:is_related_to']
            # reorganize endpoint info, output and relation
            parsed_result['endpoints'][endpoint_name].update({'output': _output, 'relation': relation, 'input': _info['get']['parameters'][0]['x-valueType']})
            parsed_result['api'][api_name]['endpoints'].append(data['servers'][0]['url'] + _name)
        return parsed_result
