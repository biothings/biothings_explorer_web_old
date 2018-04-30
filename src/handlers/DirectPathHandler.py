import requests_cache
from joblib import Parallel, delayed
import multiprocessing
import requests
import json

from biothings_explorer.api_call_handler import ApiCallHandler
from biothings_explorer.output_organizer import OutputOrganizor
from biothings_explorer.networkx_helper import NetworkxHelper
from biothings_explorer.path_planner import PathPlanner
from .basehandler import BaseHandler

requests_cache.install_cache('biothings_cache', backend='sqlite', expire_after=36000)

class DirectPathHelper:

    def __init__(self):
        self.nh = NetworkxHelper()
        self.ah = ApiCallHandler()
        self.oo = OutputOrganizor()
        self.pp = PathPlanner()

    def curie2value(self, curie):
        """
        Given an URI, e.g. http://identifiers.org/ncbigene/1017
        Return it in CURIE format, e.g. NCBIGene:1017

        Return
        ======
        CURIE
        """
        prefix = curie.split(':')[0]
        value = curie[len(prefix)+1: ]
        return value


    def assoc_curie_to_uri(self, curie):
        curie = curie.replace('assoc:', 'http://biothings.io/explorer/vocab/objects/')
        return curie

    def find_synonym(self, input_prefix, input_value):
        """
        Given a CURIE, finding all its equivalent CURIEs
        """
        # Step 1: Find all equivalent prefixes
        equivalent_prefix_paths = self.nh.find_equivalent_prefix_as_output(input_prefix, return_mode='path')
        # Step 2: Explore all paths and get all potentail equivalent CURIES
        curies = set()
        input_curie = input_prefix + ':' + input_value
        for _path in equivalent_prefix_paths:
            assert len(_path) == 3
            _temp = self.ah.input2output(_path[0], input_value, _path[1], _path[-1])
            curies = curies | self.oo.organize_synonym_output(_temp)
        curies.add(input_curie)
        return list(curies)

    def find_endpoint(self, input_type):
        """
        This function takes input_type as input, and return all endpoints which can ingest the input_type

        Return
        ======
        List of endpoints
        """
        return list(self.nh.api_map.successors(input_type))

    def expand_output(self, outputs, output_prefix):
        for _output in outputs:
            current_output_prefix = _output['output'][0]['id'].split(':')[0]
            if current_output_prefix != output_prefix:
                synonyms = self.find_synonym(current_output_prefix, self.curie2value(_output['output'][0]['id']))
                synonyms_matching_output_prefix = [_synonym for _synonym in synonyms if _synonym.startswith(output_prefix)]
                for _synonym in synonyms_matching_output_prefix:
                    _output['output'][0]['id'] = _synonym
                    yield _output
            else:
                yield _output

    def curie_input_to_output(self, input_curie, output_prefix):
        # Step 1: Find all direct paths which can connect from input_prefix to output_prefix
        paths = self.pp.find_path(input_curie.split(':')[0], output_prefix, max_no_api_used=1)
        # Setp 2: Combine all outputs
        outputs = []
        if paths:
            for _path in paths:
                _path = _path[0]
                _temp = self.ah.input2output(_path['input'], self.curie2value(input_curie), _path['endpoint'], _path['output'])
                if _temp:
                    _temp = [_doc['output'][0] for _doc in _temp]
                    for _doc in _temp:
                        _doc['edge'].update({'endpoint': _path['endpoint'], 'api': self.nh.registry.endpoint_info[_path['endpoint']]['api'], 'predicate': _path['relation'].split(':')[-1]})
                outputs += _temp
            if outputs:
                return outputs
            else:
                return {'error': 'Path is found. But no output could be found based on the input_curie given!'}
        else:
            return {'error': 'no path could be found'}

    def curie_input_to_output_auto_expand(self, input_curie, output_prefix):
        input_prefix = input_curie.split(':')[0]
        input_value = self.curie2value(input_curie)
        synonyms = self.find_synonym(input_prefix, input_value)
        outputs = []
        for _synonym in synonyms:
            outputs += self.curie_input_to_output(_synonym, output_prefix)
        return outputs

    def path_to_output(self, path, input_value, association):
        # Step 1: Get JSON document
        # Step 2: JSON2NQUADS
        jsonld_context = self.registry.endpoint_info[endpoint_name]['jsonld_context']
        nquads = self.jh.json2nquads(json_doc, jsonld_context)
        # Step 3: Extract properties from Nquads
        properties = self.jh.fetch_properties_by_association_and_prefix_in_nquads(nquads, predicate, output_uri)
        properties = [self.oo.nquads2dict(_property) for _property in properties]
        # Step 4: Reorganize data
        if association == 'assoc:EquivalentAssociation':
            return self.oo.organize_synonym_output(properties)
        else:
            return properties

    def get_json_helper(self, _endpoint, input_type, input_value):
        params = self.ah.call_api({input_type: input_value}, _endpoint)
        response = requests.get(params[0], params=params[1], headers={'Accept': 'application/json'})
        if response.status_code == 200:
            return self.ah.preprocess_json_doc(response.json(), _endpoint)
        else:
            return {}


class DirectPathHandler(BaseHandler):
    """
    This function serves as one BioThings Explorer API endpoint
    Given an input_type and input_value, 
    return all biological entities(type & value) which could be linked to this entity

    Params
    ======
    DefaultDict grouped by semantic type

    """
    def get(self):
        input_curie = self.get_query_argument('input_curie')
        output_prefix = self.get_query_argument('output_prefix')
        endpoint = self.get_query_argument('endpoint', None)
        api = self.get_query_argument('api', None)
        predicate = self.get_query_argument('predicate', None)
        results = DirectPathHelper().curie_input_to_output(input_curie, output_prefix)
        if type(results) == list:
            if endpoint:
                results = [_result for _result in results if _result['edge']['endpoint'] == endpoint]
            if api:
                results = [_result for _result in results if _result['edge']['api'] == api]
            if predicate:
                results = [_result for _result in results if _result['edge']['predicate'] == predicate]
            self.write(json.dumps({'data': results}))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "message": results['error']}))

class FindSynonymHandler(BaseHandler):
    """
    This function serves as one BioThings Explorer API endpoint
    Given an input_type and input_value, 
    return all biological entities(type & value) which could be linked to this entity

    Params
    ======
    DefaultDict grouped by semantic type

    """
    def get(self):
        input_prefix = self.get_query_argument('input_prefix')
        input_value = self.get_query_argument('input_value')
        results = DirectPathHelper().find_synonym(input_prefix, input_value)
        self.write(json.dumps({"synonyms": results}))