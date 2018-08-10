import json

from biothings_explorer.api_call_handler import ApiCallHandler
from .basehandler import BaseHandler

class RegistryHandler(BaseHandler):
    def get(self):
        registry = ApiCallHandler().registry.bioentity_info
        reorganized_output = []
        for k, v in registry.items():
            reorganized_output.append([v['prefix'], v['preferred_name'], k, v['pattern'], 
            						   v['example'], v['semantic type'], v['attribute type'], v['description']])
        self.write(json.dumps(reorganized_output))