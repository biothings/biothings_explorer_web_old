from .biothings_helper import find_annotate_api_ids, find_query_api_ids, find_value_from_output_type, query_ids_from_output_type

class Graph():
    def get_nodes_edges(self, output_dict):
        nodes = []
        edges = []
        for k, v in output_dict.items():
            nodes.append(k)
            for _value in v:
                nodes.append(_value)
                edges.append((k, _value))
        return (nodes, edges)

    def add_to_graph(self, output_dict):
        (nodes, edges) = self.get_nodes_edges(output_dict)
        self.graph.add_nodes_from(nodes)
        self.graph.add_edges_from(edges)
        print('Number of nodes added: {}. Number of edges added: {}'.format(len(nodes), len(edges)))

class IdListHandler():

    def list_handler(self, input_id_list, input_type, output_type, relation=None):
        output_id_list = []
        for _input_id in input_id_list:
            ih = IdHandler(_input_id, input_type)
            output_ids = ih.retrieve_id(output_type, relation)
            if output_ids:
                for _output_id in output_ids:
                    output_id_list.append(_output_id)
        return list(set(output_id_list))

    def list_handler_for_graph(self, input_id_list, input_type, output_type, relation=None):
        output_id_dict = {}
        for _input_id in input_id_list:
            ih = IdHandler(_input_id, input_type)
            output_ids = ih.retrieve_id(output_type, relation)
            output_id_dict[_input_id] = output_ids
        return output_id_dict

class IdHandler():
    '''
    Given id/ids and their type,
    fetch all available APIs providing annotate or query service
    fetch all IDs related by annotate or query api

    '''
    def __init__(self, ids, type):
        self._ids = ids
        self._type = type
        self.annotate_api_id = find_annotate_api_ids(self._type)
        self.query_api_id = find_query_api_ids(self._type)
        self.available_annotate_id = []
        self.available_query_id = []
        for _api, _ids in self.annotate_api_id.items():
            for _id in _ids:
                self.available_annotate_id.append(_id)
        for _api, _ids in self.query_api_id.items():
            for _id in _ids:
                self.available_query_id.append(_id)

    def available_apis(self):
        print('Available annotate APIs: {}'.format(self.annotate_api_id.keys()))
        print('Available query APIs: {}'.format(self.query_api_id.keys()))

    def available_ids(self):
        print('Available ids from annotate apis: {}'.format(self.available_annotate_id))
        print('Available ids from query apis: {}'.format(self.available_query_id))

    def retrieve_id(self, output_type, relation=None):
        if output_type in self.available_annotate_id:
            for _api, _id in self.annotate_api_id.items():
                if output_type in _id:
                    return find_value_from_output_type(_api, self._ids, output_type, relation)
        elif output_type in self.available_query_id:
            for _api, _id in self.query_api_id.items():
                if output_type in _id:
                    return query_ids_from_output_type(_api, self._type, self._ids, relation)
        else:
            print("coundn't")
