import asyncio
import aiohttp
import time
from collections import defaultdict

from .path_planner import PathPlanner
from .api_registry_parser import RegistryParser
from .id_converter import IDConverter
from .api_call_handler import ApiCallHandler
from .networkx_helper import NetworkxHelper

class SemanticQueryHelper:
    def __init__(self):
        self.pp = PathPlanner()
        self.registry = RegistryParser(readmethod='filepath', initialize=True)
        self.converter = IDConverter()
        self.ah = ApiCallHandler()
        self.nh = NetworkxHelper()

    def splitcurie(self, curie):
        prefix = curie.split(':')[0]
        value = curie[len(prefix)+1:]
        return (prefix, value)

    async def fetch_async(self, input_type, endpoint_name, output_type, input_value):
        input_type = self.registry.prefix2uri(input_type)
        output_type = self.registry.prefix2uri(output_type)
        uri_value = {input_type: input_value}
        api_call_params = self.ah.call_api(uri_value, endpoint_name)
        predicate = self.nh.find_edge_label(endpoint_name, self.registry.bioentity_info[output_type]['preferred_name'])
        if type(predicate) != list:
            predicate = predicate.replace('assoc:', 'http://biothings.io/explorer/vocab/objects/')
        else:
            predicate = [_predicate.replace('assoc:', 'http://biothings.io/explorer/vocab/objects/') for _predicate in predicate]
        try:
            response = await aiohttp.request('GET', api_call_params[0], params=api_call_params[1], headers={'Accept': 'application/json'})
        except:
            return None
        json_response = await response.json()
        final_results = []
        if type(predicate) != list:
            outputs = self.ah.extract_output(json_response, endpoint_name, output_type, predicate=predicate)
            for i in range(len(outputs)):
                if outputs[i]:
                    final_results.append({'input': (input_value, self.registry.bioentity_info[input_type]['preferred_name']), 'output': (outputs[i]),
                                          'endpoint': endpoint_name, 'target': outputs[i][0]['target']['id']})
        else:
            for _predicate in predicate:
                outputs = self.ah.extract_output(valid_responses, endpoint_name, output_type, predicate=_predicate)
            for i in range(len(outputs)):
                if outputs[i]:
                    final_results.append({'input': (input_value, self.registry.bioentity_info[input_type]['preferred_name']), 'output': (outputs[i]),
                                          'endpoint': endpoint_name, 'target': outputs[i][0]['target']['id']})
        return final_results

    async def asynchronous(self, paths):
        start = time.time()
        tasks = [asyncio.ensure_future(self.fetch_async(a, b, c, d)) for (a, b, c, d) in paths]
        results = await asyncio.wait(tasks)
        print("Process took: {:.2f} seconds".format(time.time() - start))
        return results

    def input2output(self, input_prefix, output_prefix, input_value):
        """
        Step 1: Find input & output semantic type
        Step 2: Find input synonyms
        Step 3: Find all potential paths directly connecting input and output
        Step 4: Cross check with input synonyms to construct actual path
        Step 5: Use path to get output
        Step 6: Align outputs to the final output_prefix
        """
        # Find semantic type
        input_semantic_type = self.registry.prefix2semantictype(input_prefix)
        output_semantic_type = self.registry.prefix2semantictype(output_prefix)

        # find input synonyms
        if input_semantic_type == 'gene':
            input_synonyms = self.converter.find_gene_synonym(input_value, input_prefix)[0]
        elif input_semantic_type == 'chemical':
            input_synonyms = self.converter.find_chemical_synonym(input_value, input_prefix)[0]
        else:
            input_synonyms = {input_prefix: input_value}
        # find all paths connecting input_semantic_type and output_semantic_type
        potential_paths = self.pp.find_path_between_two_semantic_types(input_semantic_type, output_semantic_type)
        # cross check input synonyms with potential paths
        actual_paths = []
        for _path in potential_paths:
            if _path[0] in input_synonyms:
                _path.append(input_synonyms[_path[0]])
                actual_paths.append(_path)
        # use actual paths to get output
        results = []
        """
        for _path in actual_paths:
            results += self.ah.input2output(_path[0], _path[-1], _path[1], _path[2])
        """
        ioloop = asyncio.get_event_loop()
        done, _ = ioloop.run_until_complete(self.asynchronous(actual_paths))
        for fut in done:
            results+= fut.result()
        #ioloop.close()
        # align output
        """
        Step 1: extract all the outputs
        Step 2: group targets based on prefix
        Step 3: convert to designated output prefix using find_synonym
        Step 4: put back to output
        """
        """
        output_targets = [self.splitcurie(_result['target']) for _result in results]
        res = defaultdict(list)
        for prefix, value in output_targets:
            res[prefix].append(value)
        """

        return results
