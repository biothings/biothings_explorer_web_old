import json

from biothings_explorer.semantic_query_helper import SemanticQueryHelper
from .basehandler import BaseHandler

class QuerySemanticsHandler(BaseHandler):
    """
    
    Params
    ======
    DefaultDict grouped by semantic type

    """
    def get(self):
        input_prefix = self.get_query_argument('input_prefix')
        input_value = self.get_query_argument('input_value')
        output_prefix = self.get_query_argument('output_prefix')
        sh = SemanticQueryHelper()
        outputs = sh.input2output(input_prefix, output_prefix, input_value)
        if outputs:
            self.write(json.dumps({'data': outputs}))
        else:
            self.set_status(400)
            self.write(json.dumps({'error message': "no outputs found!"}))