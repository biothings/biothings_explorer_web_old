import networkx as nx
import os, sys

from .api_call_handler import ApiCallHandler
from .api_registry_parser import RegistryParser
from .visjupyter_helper import find_edge_label, path2Graph, explore2Graph
from .utils import output2input

# add path for the config folder
#sys.path.append('/Users/kevinxin/Documents/myvariant.info/json-ld/bt_explorer_web_development/config_folder/bt_explorer_2')
#from .config import LOG_FOLDER

formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#logging.basicConfig(level=logging.DEBUG, filename=os.path.join(LOG_FOLDER, 'debug.log'), format=formatter)

class BioThingsExplorer:
    def __init__(self):
        self.graph_id = 1
        self.apiCallHandler = ApiCallHandler()
        self.registry = RegistryParser()
        self.api_map = self.registry.api_map
        self.temp_G = nx.MultiDiGraph()
        self.paths = None
        self.selected_path = None
        self.graph_id = 0
        self.temp_results = {}


    """
    This should be moved to helper function
    """
    def path_conversion(self, pathList, relation_filter=None):
        """
        converted path from list to dict
        Example: [1, 2, 3, 4, 5] ==> [{'input': 1, 'endpoint': 2,
                                       'output': 3, relation: '...'},
                                      {'input': 3, 'endpoint': 4,
                                      'output': 5, relation: '...'}]

        Params
        ======
        pathList: (list)
            A list containing one path from start to end
        relation_filter: (str)
            user specified edge label
        """
        pathDict = []
        for i in range(0, len(pathList) - 1, 2):
            list2dict = {'input': pathList[i], 'endpoint': pathList[i + 1],
                         'output': pathList[i + 2]}
            list2dict.update({'relation': find_edge_label(self.api_map,
                              pathList[i + 1], pathList[i + 2],
                relation_filter)})
            pathDict.append(list2dict)
        return pathDict

    def find_path(self, start, end, max_no_api_used=4, intermediate_nodes=[], excluded_nodes=[], relation_filter=None, dictformat=True, display_graph=True):
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
        if start not in self.api_map.nodes() or end not in self.api_map.nodes():
            print('the start and end position is not in the api_map')
            return
        visited = [start]
        stack = [self.api_map.successors(start)]
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
                    stack.append(self.api_map.successors(child))
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
        self.temp_G = path2Graph(self.paths)
        if not dictformat:
            return final_results
        elif display_graph:
            self.graph_id += 1
            #return draw_graph(self.temp_G, graph_id=self.graph_id)
        else:
            return self.paths

    def find_output(self, path, input_value, display_graph=True, return_networkx=True):
        """
        Given a user chosen path from input to output, together with
        a user given input_value
        return a graph displaying input and output, together with all
        intermediate results

        Params
        ======
        path: (list)
            containing (intermediate) steps from input to output
        input_value: (list)
            input for the path to begin with
        display_graph:
            whether to display the graph on jupyter notebook or not
            if not, return a networkx multigraph containing all info
        TODO: handle multiple parameters
        Return:
            visJs graph display
        """
        self.selected_path = path
        self.temp_results = {}
        path_input = input_value
        for i, _path in enumerate(path):
            print('Currently working on path {}. The path connects from {} to {} using {}!!'.format(i, _path['input'], _path['output'],
                                     _path['endpoint']))
            path_output = self.apiCallHandler.input2output(_path['input'],
                                                           path_input,
                                                           _path['endpoint'],
                                                           _path['output'],
                                                           _path['relation'])
            if path_output:
                if len(path_output) > 20:
                    self.temp_results.update({i: path_output[:20]})
                    path_input = output2input(path_output)[:20]
                else:
                    self.temp_results.update({i: path_output})
                    path_input = output2input(path_output)
            else:
                print('No results could be found for the given path!! The \
                    exploration ended!')
                self.temp_G = explore2Graph(self.temp_results)
                self.graph_id += 1
                if display_graph:
                    return
                elif return_networkx:
                    return self.temp_G
                else:
                    return self.temp_results
            print('Done!!!')
        self.temp_G = explore2Graph(self.temp_results)
        self.graph_id += 1
        if display_graph:
            return
        elif return_networkx:
            return self.temp_G
        else:
            return self.temp_results

