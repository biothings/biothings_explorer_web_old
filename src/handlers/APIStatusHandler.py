from .basehandler import BaseHandler
import os, sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import api_status_file

class APIStatusHandler(BaseHandler):
    def get(self):
        with open(api_status_file, 'r') as f:
            api_status = json.load(f)
            self.write(json.dumps(api_status))
