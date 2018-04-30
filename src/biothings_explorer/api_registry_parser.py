from urllib.parse import urljoin
import networkx as nx
import os.path
from collections import defaultdict

from .utils import readFile
from .config import FILE_PATHS
from .jsonld_processor import JSONLDHelper


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
        self.jh = JSONLDHelper()
        self.api_map = nx.MultiDiGraph()
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
            self.construct_api_road_map()

    def read_id_mapping_file(self):
        """
        read in the ID-MAPPING.csv file
        and parse it into bioentity_info dictionary
        The dictionary key is the URI, and it's value contains registry_identifier, etc.
        """
        data = readFile(self.id_mapping_path)
        # turn data frame into a dictionary and store in bioentity_info
        for index, row in data.iterrows():
            self.bioentity_info[row['URI']] = {'description': row['Description'], 'preferred_name': row['Recommended name'], 'semantic type': row['Semantic Type']}
        return self.bioentity_info

    def prefix2uri(self, prefix, verbose=False):
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
        if verbose:
            print('No URI could be found for the prefix provided: {}'.format(prefix))

    def prefix2semantictype(self, prefix, verbose=False):
        """
        Given a bio-entity in prefix format, return its semantic type

        Params
        ======
        prefix: (str)
            bio-entity in prefix format

        Return
        ======
        bio-entity in its semantic type, e.g. GENE, VARIANT
        """
        for k, v in self.bioentity_info.items():
            if v['preferred_name'] == prefix:
                return self.bioentity_info[k]['semantic type']
        # print error message if no URI was found
        if verbose:
            print('No URI could be found for the prefix provided: {}'.format(prefix))

    def semantictype2prefix(self, semantic_type):
        """
        Given a semantic type, e.g. gene, variant, return all prefixes corresponding to the semantic type

        Params
        ======
        semantic_type: (str)

        Return
        ======
        List of prefixes
        """
        for k, v in self.bioentity_info.items():
            if v['semantic type'] == semantic_type:
                yield v['preferred_name']

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
            # get endpoint outputs from x-responseValueType
            if 'x-responseValueType' in _info['get']['responses']['200']:
                _output = [_item['valueType'] for _item in _info['get']['responses']['200']['x-responseValueType'] if _item['valueType'] in self.bioentity_info]
            else:
                continue
            # get endpoint inputs from x-valueType
            if 'x-valueType' in _info['get']['parameters'][0]:
                _input = [_item for _item in _info['get']['parameters'][0]['x-valueType'] if _item in self.bioentity_info]
            else:
                continue
            endpoint_name = data['servers'][0]['url'] + _name
            parsed_result['endpoints'].update({endpoint_name: _info})
            # extract relationship info from the json-ld context file
            relation = {}
            # get relationship between inputs and outputs from JSON-LD context files
            if 'x-JSONLDContext' in _info['get']['responses']['200']:
                if self.readmethod == 'http':
                    jsonld_path = urljoin(self.registry_path, _info['get']['responses']['200']['x-JSONLDContext'])
                elif self.readmethod == 'filepath':
                    jsonld_path = os.path.join(self.registry_path, _info['get']['responses']['200']['x-JSONLDContext'])
                if 'disease-ontology' in endpoint_name:
                    relation = {}
                    for _op in _output:
                        relation[_op] = set(['assoc:EquivalentAssociation'])
                elif 'homolog' in endpoint_name:
                    relation = {}
                    for _op in _output:
                        relation[_op] = set(['assoc:GeneToGeneHomologyAssociation'])
                else:
                    relation = self.jh.jsonld_relation_parser(readFile(jsonld_path))
                parsed_result['endpoints'][endpoint_name].update({'jsonld_context': jsonld_path})

            #for _op in _output:
            #    if _op not in relation:
            #        relation[_op] = ['ont:isRelatedTo']
            # reorganize endpoint info, output and relation
            associations = set()
            for _assoc in relation.values():
                associations = associations | _assoc
            associations = [_assoc.replace("assoc:", "http://biothings.io/explorer/vocab/objects/") for _assoc in associations]
            parsed_result['endpoints'][endpoint_name].update({'output': _output, 'relation': relation, 'associations': associations, 'input': _input, 'api': data['servers'][0]['url']})
            parsed_result['api'][api_name]['endpoints'].append(data['servers'][0]['url'] + _name)
        return parsed_result

    def construct_api_road_map(self):
        """
        This function will add all API, endpoint, input/output info
        as well as the relationship between endpoint and output
        into the networkx MultiGraph.

        Return
        ======
        MultiDiGraph
        """
        # add nodes and edges between api and endpoints
        for _api, _info in self.api_info.items():
            self.api_map.add_node(_api, type='api', color='red')
            for _endpoint in _info['endpoints']:
                self.api_map.add_node(_endpoint, type='endpoint', color='blue')
                self.api_map.add_edge(_api, _endpoint, label='has_endpoint')
        # add endpoint and input/output to the graph
        for _endpoint, _info in self.endpoint_info.items():
            for _input in _info['input']:
                preferred_name = self.bioentity_info[_input]['preferred_name']
                self.api_map.add_node(preferred_name, type='bioentity', color='yellow')
                self.api_map.add_edge(preferred_name, _endpoint, label='has_input')
            for _output in _info['output']:
                preferred_name = self.bioentity_info[_output]['preferred_name']
                self.api_map.add_node(preferred_name, type='bioentity', color='yellow')
                if _output in _info['relation']:
                    relations = _info['relation'][_output]
                    for _relation in relations:
                        self.api_map.add_edge(_endpoint, preferred_name, label=_relation)
        return self.api_map