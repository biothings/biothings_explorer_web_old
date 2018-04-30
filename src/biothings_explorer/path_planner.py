from .api_registry_parser import RegistryParser
from .jsonld_processor import JSONLDHelper
from .output_organizer import OutputOrganizor
from .networkx_helper import NetworkxHelper

class PathPlanner:
    def __init__(self):
        self.registry = RegistryParser(readmethod='filepath', initialize=True)
        self.nh = NetworkxHelper()
        self.paths = []

    def path_conversion(self, pathList, relation_filter=None):
        """
        converted path from list to dict
        Example: [1, 2, 3, 4, 5] ==> [{'input': 1, 'endpoint': 2, 'output': 3, relation: '...'},
                                      {'input': 3, 'endpoint': 4, 'output': 5, relation: '...'}]

        Params
        ======
        pathList: (list)
            A list containing one path from start to end
        relation_filter: (str)
            user specified edge label
        """
        pathDict = []
        for i in range(0, len(pathList)-1, 2):
            list2dict = {'input': pathList[i], 'endpoint': pathList[i+1],
                         'output': pathList[i+2]}
            list2dict.update({'relation': self.nh.find_edge_label(pathList[i+1], pathList[i+2], relation_filter)})
            pathDict.append(list2dict)
        return pathDict

    def find_path(self, start, end, max_no_api_used=3, intermediate_nodes=[], excluded_nodes=[], relation_filter=None, dictformat=True):
        """
        return paths connecting start and end bio-entity specified

        Params
        ======
        start: (str)
            path start point
        end: (str)
            path end point
        max_no_api_used: (int)
            maximum number of api(s) included in the path
        intermediate_nodes: (list)
            node(s) which the path must contain
        excluded_nodes: (list)
            node(s) which the path must not contain
        relation_filter: (string)
            specify the edge label

        Return
        ======
        list of paths, each path is a list containing the nodes
        """
        self.paths = None
        self.selected_path = None
        cutoff = max_no_api_used * 2 + 1
        if cutoff < 1:
            print('please specify max_no_api_used with a number >= 1')
            return
        if start not in self.registry.api_map.nodes() or end not in self.registry.api_map.nodes():
            print('the start and end position is not in the api_map')
            return
        visited = [start]
        stack = [self.registry.api_map.successors(start)]
        paths = []
        final_results = []
        while stack:
            children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                visited.pop()
            elif len(visited) < cutoff:
                if child == end:
                    new_path = visited + [end]
                    if new_path not in paths:
                        paths.append(visited + [end])
                elif child not in visited:
                    visited.append(child)
                    stack.append(self.registry.api_map.successors(child))
            else:
                if child == end or end in children:
                    new_path = visited + [end]
                    if new_path not in paths:
                        paths.append(visited + [end])
                stack.pop()
                visited.pop()
        for _path in paths:
            # user specify both excluded_nodes and intermediate_nodes
            if excluded_nodes and intermediate_nodes and len(set(excluded_nodes) - set(_path)) == len(excluded_nodes)\
                    and not set(intermediate_nodes) - set(_path):
                final_results.append(_path)
            # user only specify excluded_nodes
            elif excluded_nodes and len(set(excluded_nodes) - set(_path)) == len(excluded_nodes) and not intermediate_nodes:
                final_results.append(_path)
            # user only specify intermediate nodes
            elif intermediate_nodes and not set(intermediate_nodes) - set(_path) and not excluded_nodes:
                final_results.append(_path)
            # user specify neither excluded_nodes nor intermediate_nodes
            elif not intermediate_nodes and not excluded_nodes:
                final_results.append(_path)
            else:
                continue
        self.paths = [self.path_conversion(_path, relation_filter) for _path in final_results]
        if not dictformat:
            return final_results
        else:
            return self.paths

    def path_filter_for_direct_relation(self, paths):
        """
        This function filter paths for direct relation
        e.g. gene-gene-drug-drug, gene-gene-drug, gene-drug-drug, gene-drug
        """
        filtered_paths = []
        for path in paths:
            # case 1, when there are 3 sub-paths
            # In this case, check whether the relationship in first and last sub-path is 'equivalent'
            if len(path) == 3 and path[0]['relation'] == path[-1]['relation'] == 'assoc:EquivalentAssociation':
                filtered_paths.append(path)
            # case 2, when there are 2 sub-paths
            # In this case, check whether the first or the last sub-path relation is 'equivalent'
            elif len(path) == 2 and (path[0]['relation'] == 'assoc:EquivalentAssociation' or path[1]['relation'] == 'assoc:EquivalentAssociation'):
                filtered_paths.append(path)
            # case 3, when there are only 1 sub-paths, directly select it
            elif len(path) == 1:
                filtered_paths.append(path)
        return filtered_paths

    def find_path_between_two_semantic_types(self, input_type, output_type, filter_duplicate=True):
        """
        
        """
        paths = []
        available_input_prefixes = list(self.registry.semantictype2prefix(input_type))
        available_output_prefixes = list(self.registry.semantictype2prefix(output_type))
        for _input_prefix in available_input_prefixes:
            for _output_prefix in available_output_prefixes:
                if self.nh.find_direct_paths_connecting_input_and_output(_input_prefix, _output_prefix):
                    paths += self.nh.find_direct_paths_connecting_input_and_output(_input_prefix, _output_prefix)
        if filter_duplicate:
            new_paths = []
            apis = []
            for _path in paths:
                if _path[1] not in apis:
                    apis.append(_path[1])
                    new_paths.append(_path)
            return new_paths
        return paths