import os
import sys
from os import path

lib_path = os.path.abspath(os.path.join('..', 'biothings_explorer'))
sys.path.append(path.dirname(path.dirname(path.abspath(lib_path))))
from biothings_explorer import BioThingsExplorer


color_dict = {
              'gene': 'rgba(55, 230, 84, 0.93)',
              'chemical': 'rgba(230, 55, 218, 0.93)', 
              'protein': 'rgba(55, 227, 230, 0.6)',
              'variant': 'rgba(230, 174, 55, 0.83)', 
              'anatomy': 'rgba(86, 28, 144, 0.3)',
              'phenotype': 'rgba(28, 86, 144, 0.3)', 
              'pathway': 'rgba(230, 55, 116, 0.63)',
              'disease': 'rgba(166, 55, 230, 0.84)', 
              'transcript': 'rgba(100, 88, 77, 0.4)',
              'organism': 'rgba(10, 133, 177, 0.4)',
              'structure': 'rgba(8, 233, 7, 0.4)', 
              'ontology': 'rgba(99,123,4,0.4)',
              'bioassay': "rgba(100, 100, 100, 0.3)"}

class HandlerUtils:
    def __init__(self):
        self.bt_explorer = BioThingsExplorer()

    def find_edge_label(self, G, source, target, relation=None):
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
        if (source, target) not in G.edges():
            print('The given pair source-target pair ({}, {}) is not in the graph!'.format(source, target))
            return None
        edge_labels = [v['label'] for k, v in G.get_edge_data(source, target).items()]
        if len(edge_labels) == 1:
            return edge_labels[0]
        elif len(edge_labels) > 1 and not relation:
            return edge_labels
        elif len(edge_labels) > 1 and relation and relation in edge_labels:
            return relation
        else:
            return None

    def label2color(self, label):
        uri = self.bt_explorer.registry.prefix2uri(label)
        if uri:
            return color_dict[self.bt_explorer.registry.bioentity_info[uri]['semantic type']]
        else:
            return "rgba(250, 0, 0, 1.0)"

    ###########################################################################
    # Sample Input: (
    #                 [('ncbigene', 'http://mygene.info/v1/'),
    #                  ('ncbigene', 'http://myvariant.info/v1/'),
    #                  ('http://mygene.info/v1/', 'hgnc.symbol'),
    #                  ('http://myvariant.info/v1/', 'hgnc.symbol')])
    # The input is the edges returned from networkx
    # We need to take the input and feed it into plotly sankey plot
    # The output which plotly sankey plot accepts looks like this:
    # Sample Output:
    # {
    #    "label": ["ncbigene", "MyGene.info/v1/query",
    #             "MyVariant.info/v1/query", "hgnc.symbol"],
    #   "source": [0, 0, 1, 2], # represent the index in label
    #    "target": [1, 2, 3, 3],
    #    "value": [1,1,1,1] # edge weight, this doesn't apply for our use case
    # }
    # Issue: plotly fails to work if there are too many nodes
    ###########################################################################

    def networkx_to_plotly(self, edges, duplicates_not_allowed=[]):
        # initialize the output json doc
        output_json = {'labels': [], 'colors': [], 'source': [], 'target': [], 'value': [], 'edge_labels': []}
        # loop through each edge, load the first element into source
        # and load the second element into target
        # load all unique elements to the nodes
        idx = 0
        input_idx = {}
        output_idx = {}
        for _edge in edges:
            if _edge[0] in duplicates_not_allowed:
                if _edge[0] not in output_json['labels']:
                    input_idx[_edge[0]] = idx
                    output_idx[_edge[0]] = idx
                    idx += 1
                    output_json['labels'].append(_edge[0])
                    output_json['colors'].append(self.label2color(_edge[0]))
            elif _edge[0] not in input_idx:
                input_idx[_edge[0]] = idx
                idx += 1
                output_json['labels'].append(_edge[0])
                output_json['colors'].append(self.label2color(_edge[0]))
            output_json['source'].append(input_idx[_edge[0]])
            if _edge[1] in duplicates_not_allowed:
                if _edge[1] not in output_json['labels']:
                    input_idx[_edge[1]] = idx
                    output_idx[_edge[1]] = idx
                    idx += 1
                    output_json['labels'].append(_edge[1])
                    output_json['colors'].append(self.label2color(_edge[1]))
            elif _edge[1] not in output_idx:
                output_idx[_edge[1]] = idx
                idx += 1
                output_json['labels'].append(_edge[1])
                output_json['colors'].append(self.label2color(_edge[1]))
            output_json['target'].append(output_idx[_edge[1]])
            output_json['edge_labels'].append(_edge[2])
            if type(_edge[2]) == list:
                output_json['value'].append(1*len(_edge[2]))
            else:
                output_json['value'].append(1)
        return output_json

    def construct_knowledge_map(self):
        triples = []
        for _endpoint, _endpoint_info in self.bt_explorer.registry.endpoint_info.items():
            relation = _endpoint_info['relation']
            inputs = _endpoint_info['input']
            for _input in inputs:
                _input_curie = self.bt_explorer.registry.bioentity_info[_input]['prefix']
                _input_type = self.bt_explorer.registry.bioentity_info[_input]['semantic type']
                for _output, _relation in relation.items():
                    _output_curie = self.bt_explorer.registry.bioentity_info[_output]['prefix']
                    _output_type = self.bt_explorer.registry.bioentity_info[_output]['semantic type']
                    for _relate in _relation:
                        triples.append({'subject': {'prefix': _input_curie, 'semantic_type': _input_type}, 
                                       'object': {'prefix': _output_curie, 'semantic_type': _output_type}, 
                                       'predicate': _relate.split(':')[-1], 'endpoint': _endpoint})
        return triples
