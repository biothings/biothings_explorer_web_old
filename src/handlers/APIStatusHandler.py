from .basehandler import BaseHandler
import os, sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import api_status_file, database_status_file

class APIStatusHandler(BaseHandler):
    def get(self):
        output_format = self.get_query_argument('format', None)
        with open(api_status_file, 'r') as f:
            api_status = json.load(f)
            if not output_format:
                self.write(json.dumps(api_status))
            else:
                reorganized_output = []
                for k, v in api_status['status'].items():
                    reorganized_output.append([k, v])
                self.write(json.dumps(reorganized_output))

class DatabaseStatusHandler(BaseHandler):
    def get(self):
        output_format = self.get_query_argument('format', None)
        with open(database_status_file, 'r') as f:
            database_status = json.load(f)
            if not output_format:
                self.write(json.dumps(database_status))
            else:
                reorganized_output = []
                for k, v in database_status['status'].items():
                    for _item in v:
                        reorganized_output.append([_item['source_name'], _item['source_version'], k])
                print(reorganized_output)
                self.write(json.dumps(reorganized_output))
