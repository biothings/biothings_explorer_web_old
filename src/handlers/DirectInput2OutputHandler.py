import json

from biothings_explorer.api_call_handler import ApiCallHandler
from .basehandler import BaseHandler


class DirectInput2OutputHandler(BaseHandler):
    """
    This function serves as one BioThings Explorer API endpoint
    Given input_type, input_value and output_type
    return all API call outputs which could lead to the output_type

    Params
    ======
    DefaultDict grouped by semantic type

    """
    def get(self):
        # read in parameters, all parameters are required
        ah = ApiCallHandler()
        input_prefix = self.get_query_argument('input_prefix')
        input_value = self.get_query_argument('input_value')
        output_prefix = self.get_query_argument('output_prefix')
        #endpoint = self.get_query_argument('endpoint', None)

        # convert from prefix to uri
        input_uri = ah.registry.prefix2uri(input_prefix)
        output_uri = ah.registry.prefix2uri(output_prefix)
        if not input_uri:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "message": "Your input prefix " + input_prefix + " is not in the registry!"}))
            self.finish()
        if not output_uri:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "message": "Your output prefix " + output_prefix + " is not in the registry!"}))
            self.finish()

        # Step 1: Find all endpoints which could connect from input_type to output_type
        endpoints = ah.api_endpoint_locator(input_uri, output_uri)
        if not endpoints:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "message": "No endpoints could be found to connect " + input_prefix + " to " + output_prefix + "!"}))
            self.finish()
        # Step 2: Make calls to all these API endpoints, and extract the output
        outputs = []
        # loop through each endpoint
        # this function should ultimately be modified using Asyncio or using multi-threading
        for _endpoint in endpoints:
            temp_output = ah.input2output(input_prefix, input_value, _endpoint, output_prefix)
            outputs += temp_output

        if outputs:
            self.write(json.dumps({'data': outputs}))
        # handle cases where no output could be extracted!
        else:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "message": "Endpoints could be located connecting " + input_prefix +
                                   " to " + output_prefix + ". The endpoints are " + str(endpoints) +
                                   ". However, no output could be found using the endpoint!"}))
