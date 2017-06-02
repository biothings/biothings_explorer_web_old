from biothings_client import get_client


class ClientRedirect:
    def __init__(self):
        self.mv = get_client("variant")
        self.mg = get_client("gene")
        self.md = get_client("drug")

    def annotate(self, id, api, fields=None):
        '''
        return client based on API name and annotate information
        fields: only return specific field(s) of the record
        '''
        if api == 'myvariant.info':
            return self.mv.getvariant(id, fields=fields)
        elif api == 'mygene.info':
            return self.mg.getgene(id, fields=fields)
        elif api == 'mydrug.info':
            return self.md.getdrug(id, fields=fields)
        else:
            print("{} doesn't have a python client, please refer to the url, and use get_json_doc method for further analysis".format(api))

    def query(self, api, query_info, fields=None, fetch_all=True):
        '''
        return client based on API name and query information
        fetch_all: return every record related to this query, by default is true
        fields: only return specific field(s) of the record
        '''
        if api == 'myvariant.info':
            return self.mv.query(query_info, fields=fields, fetch_all=fetch_all)
        elif api == 'mygene.info':
            return self.mg.query(query_info, fields=fields, fetch_all=fetch_all)
        elif api == 'mydrug.info':
            return self.md.query(query_info, fields=fields, fetch_all=fetch_all)
        else:
            print("{} doesn't have a python client, please refer to the url, and use get_json_doc method for further analysis".format(api))

    def get_id_list(self, api, query_info, fetch_all=True):
        '''
        return a list of ids related to the query info
        '''
        if fetch_all:
            id_list = [_record['_id'] for _record in self.query(api, query_info, fields='_id', fetch_all=fetch_all)]
        else:
            id_list = [_record['_id'] for _record in self.query(api, query_info, fields='_id', fetch_all=fetch_all)['hits']]
        print('Number of IDs from {} related to this query {} is : {}'.format(api, query_info, len(id_list)))
        return id_list
