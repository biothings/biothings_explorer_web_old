import visJS2jupyter.visJS_module
import networkx as nx

def draw_graph(G, graph_id=1):
    """
    Given a networkx multiDiGraph,
    Display it on the jupyter notebook cell block
    using visJS2jupyter

    params
    ======
    G: (networkx MultiDigraph)
        a networkx graph consisting of nodes, edges
    graph_id: (int)
        for displaying multiple graphs in the same jupyter notebook,
        should increase one when a new graph is added
    """
    degree = {}
    for _node in G.nodes():
        degree.update({_node: 1})
    bc = nx.betweenness_centrality(G)
    nx.set_node_attributes(G, name='degree', values=degree)
    nx.set_node_attributes(G, name='betweenness_centrality', values=bc)
    pos = nx.circular_layout(G)
    nodes_dict = [{"id": n, "color": G.node[n]['color'], "degree": nx.degree(G, n), "x": pos[n][0]*1000, "y": pos[n][0]*1000} for n in G.nodes()]
    edges = []
    for _edge in set(G.edges()):
        labels = G.edge[_edge[0]][_edge[1]].values()
        for _label in labels:
            edges.append((_edge[0], _edge[1], _label['label']))
    node_map = dict(zip(G.nodes(), range(len(G.nodes()))))  # map to indices for source/target in edges
    edges = G.edges(keys=True)
    edges_dict = [{"source": node_map[edges[i][0]], "target": node_map[edges[i][1]],
                  "color": "pink", "id": G.edge[edges[i][0]][edges[i][1]][edges[i][2]]['label']} for i in range(len(edges))]
    return visJS2jupyter.visJS_module.visjs_network(nodes_dict, edges_dict,
                                                    node_size_multiplier=3,
                                                    node_size_transform='',
                                                    node_color_highlight_border='red',
                                                    node_color_highlight_background='#D3918B',
                                                    node_color_hover_border='blue',
                                                    node_color_hover_background='#8BADD3',
                                                    node_font_size=25,
                                                    edge_arrow_to=True,
                                                    physics_enabled=True,
                                                    edge_color_highlight='#8A324E',
                                                    edge_color_hover='#8BADD3',
                                                    edge_width=3,
                                                    max_velocity=15,
                                                    min_velocity=1,
                                                    edge_smooth_enabled=True)

def find_edge_label(G, source, target, relation=None):
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
    edge_labels = [v['label'] for k, v in G.edge[source][target].items()]
    if len(edge_labels) == 1:
        return edge_labels[0]
    elif len(edge_labels) > 1 and not relation:
        return edge_labels
    elif len(edge_labels) > 1 and relation and relation in edge_labels:
        return relation
    else:
        return None

def path2Graph(paths):
    """
    Given a list of paths, convert it to networkx MulitDiGraph format

    Parmas
    ======
    paths: (list)
        list of paths connecting from A to B

    Return
    ======
        MultiDiGraph
    """
    G = nx.MultiDiGraph()
    for _path in paths:
        for _subpath in _path:
            G.add_node(_subpath['endpoint'], type='endpoint', color='blue')
            G.add_node(_subpath['input'], type='bioentity', color='yellow')
            G.add_node(_subpath['output'], type='bioentity', color='yellow')
            G.add_edge(_subpath['input'], _subpath['endpoint'], label='has_input')
            if type(_subpath['relation']) == list:
                for _relation in _subpath['relation']:
                    G.add_edge(_subpath['endpoint'], _subpath['output'], label=_relation)
            else:
                G.add_edge(_subpath['endpoint'], _subpath['output'], label=_subpath['relation'])
    return G

def explore2Graph(exploreresults):
    """
    Given path exploration results, convert it to networkx MultiDiGraph format

    Params
    ======
    exploreresults: (dict)
        dict key represents layer, dict value represents input and output

    Return
    ======
        networkx multiDiGraph
    """
    color_schema = {0: 'red', 1: 'blue', 2: 'green', 3: 'yellow', 4: 'pink', 5: 'black'}
    G = nx.MultiDiGraph()
    for layer, results in exploreresults.items():
        for _result in results:
            if 'input' in _result:
                _input = _result['input'][1] + ':' + _result['input'][0]
                if layer == 0:
                    G.add_node(_input, type='bioentity', color=color_schema[layer])
                if 'output' in _result:
                    output_type = _result['output'][1]
                    i = 0
                    for _output_result in _result['output'][0]:
                        if type(_output_result[0]) == str:
                            _output = output_type + ':' + _output_result[0]
                        else:
                            _output = output_type + ' ' + str(i)
                            i += 1
                        G.add_node(_output, type='bioentity', color=color_schema[layer+1])
                        G.add_edge(_input, _output, label=_output_result[1])
    return G

