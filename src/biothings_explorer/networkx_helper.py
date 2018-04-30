import networkx as nx
from .api_registry_parser import RegistryParser

class NetworkxHelper:
    def __init__(self):
        self.registry = RegistryParser(readmethod='filepath', initialize=True)
        self.G = self.registry.api_map

    def find_edge_label(self, source, target, relation=None):
        """
        Given a MultiDiGraph, together with a source, target pair
        Return the edge label info associated with the (source, target) pair
        1) If only one label exists, return the label
        2) When multiple label exists, if relation parameter is in the label(s), return the relation parameter
        3) If relation parameter not in the labels, return None

        Parmas
        ======
        G: (multiDiGraph)
            a multiDiGraph containaing nodes, edges and labels
        source: (multiDiGraph node)
        target: (multiDiGraph node)
        relation:
            The label given by user, default is None

        Return
        ======
            label info for the source target pair
        """
        if (source, target) not in self.G.edges():
            print('The given pair source-target pair ({}, {}) is not in the graph!'.format(source, target))
            return None
        edge_labels = [v['label'] for k, v in self.G.get_edge_data(source, target).items()]
        if len(edge_labels) == 1:
            return edge_labels[0]
        elif len(edge_labels) > 1 and not relation:
            return edge_labels
        elif len(edge_labels) > 1 and relation and relation in edge_labels:
            return relation
        else:
            return None

    def find_equivalent_prefix_as_output(self, input_prefix, return_mode='prefix'):
        """
        Given an input_prefix, return its equivalent prefix by traversing the knowledge graph
        1) Find all API endpoints taking the input_prefix
        2) Look for the edge label of the API endpoints
        3) Return the output if the edge label is 'assoc:EquivalentAssociation'

        Return
        ======
        if return_mode is 'prefix', then just return equivalent prefixes
        if return_mode is 'path', then return paths for retrieving the equivalent prefix
        """
        equivalent_prefixes = set()
        paths = []
        endpoints_taking_input_prefix = self.G[input_prefix]
        for _endpoint in endpoints_taking_input_prefix:
            output_edge = self.G[_endpoint]
            for _output in output_edge:
                edges = output_edge[_output]
                for k, edge_info in edges.items():
                    if edge_info['label'] == 'assoc:EquivalentAssociation':
                        equivalent_prefixes.add(_output)
                        paths.append([input_prefix, _endpoint, _output])
        if return_mode == 'prefix':
            return list(equivalent_prefixes)
        else:
            return paths

    def find_equivalent_prefix_as_input(self, output_prefix, return_mode='prefix'):
        equivalent_prefixes = set()
        paths = []
        endpoints_producing_output_prefix = self.G.predecessors(output_prefix)
        for _endpoint in endpoints_producing_output_prefix:
            edges = self.G.get_edge_data(_endpoint, output_prefix)
            for k, edge_info in edges.items():
                if edge_info['label'] == 'assoc:EquivalentAssociation':
                    for _input in self.G.predecessors(_endpoint):
                        equivalent_prefixes.add(_input)
                        paths.append([_input, _endpoint, output_prefix])
        if return_mode == 'prefix':
            return list(equivalent_prefixes)
        else:
            return paths


    def find_direct_paths_connecting_input_and_output(self, input_prefix, output_prefix, edge_label=None):
        """
        Given an input_prefix and an output_prefix,
        check whether there are API endpoints which directly connects the two prefixes

        Return
        ======
        Paths connecting the two prefixes in list format
        """
        paths = []
        if input_prefix in self.G:
            endpoints_taking_input_prefix = self.G[input_prefix]
            for _endpoint in endpoints_taking_input_prefix:
                output_edge = self.G[_endpoint]
                for _output in output_edge:
                    if _output == output_prefix:
                        if not edge_label:
                            paths.append([input_prefix, _endpoint, output_prefix])
                        else:
                            for k, edge_info in output_edge[_output].items():
                                if edge_info['label'] == edge_label:
                                    paths.append([input_prefix, _endpoint, output_prefix])
        return paths
