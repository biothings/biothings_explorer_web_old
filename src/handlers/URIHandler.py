import json

from biothings_explorer.api_registry_handler import RegistryParser
from .basehandler import BaseHandler

class BioThingsURIHandler(BaseHandler):
    def get(self, prefix):
        registry = RegistryParser(readmethod='filepath', initialize=True)
        uri = 'http://biothings.io/explorer/vocab/terms/' + prefix
        print(uri)
        if uri in registry.bioentity_info:
            print('in registry')
            self.write(json.dumps(registry.bioentity_info[uri]))
        elif (uri + '/') in registry.bioentity_info:
            self.write(json.dumps(registry.bioentity_info[uri + '/']))