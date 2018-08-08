import json

from biothings_explorer.api_call_handler import ApiCallHandler
from .basehandler import BaseHandler

class RegistryHandler(BaseHandler):
    def get(self):
        registry = ApiCallHandler().registry.bioentity_info
        reorganized_output = []
        for k, v in registry.items():
            reorganized_output.append([v['preferred_name'], k, v['description'], v['semantic type']])
        self.write(json.dumps(reorganized_output))