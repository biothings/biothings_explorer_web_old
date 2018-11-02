import json

from biothings_explorer.api_call_handler import ApiCallHandler
from .basehandler import BaseHandler

class RegistryHandler(BaseHandler):
    def get(self):
        prefix = self.get_query_argument('prefix', None)
        registry = ApiCallHandler().registry.bioentity_info
        reorganized_output = []
        if not prefix:
            for k, v in registry.items():
                reorganized_output.append([v['prefix'], v['preferred_name'], k, v['pattern'], 
                                           v['example'], v['semantic type'], v['attribute type'], v['description']])
            self.write(json.dumps(reorganized_output))
        else:
            output = None
            for k, v in registry.items():
                if v['prefix'].lower() == prefix.lower():
                    output = {'prefix': v['prefix'], 'uri': k, 'preferred_name': v['preferred_name'],
                              'example': v['example'], 'semantic_type': v['semantic type'],
                              'pattern': v['pattern'], 'attribute_type': v['attribute type'],
                              'description': v['description']}
            if output:
                self.write(json.dumps(output))
            else:
                self.set_status(400)
                self.write(json.dumps({"status": 400, 'error message': prefix + ' is not in the registry!'}))
                self.finish()
