import json

from biothings_explorer.api_call_handler import ApiCallHandler
from .basehandler import BaseHandler

class BioThingsURIHandler(BaseHandler):
    def get(self, prefix):
        registry = ApiCallHandler().registry
        uri = 'http://biothings.io/explorer/vocab/terms/' + prefix.strip('/')
        if uri in registry.bioentity_info:
            self.write(json.dumps(registry.bioentity_info[uri]))
        elif (uri + '/') in registry.bioentity_info:
            self.write(json.dumps(registry.bioentity_info[uri + '/']))
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, 'error message': "URI not found"}))
            self.finish()