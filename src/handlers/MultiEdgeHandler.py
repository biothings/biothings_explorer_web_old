import json
from biothings_explorer import BioThingsExplorer
from .basehandler import BaseHandler


class DictQuery(dict):

    def get(self, path, default=None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break

        return val


class MultiEdgeHandler(BaseHandler):

    """
    This function serves as one BioThings Explorer API endpoint
    Given input_type, input_value and output_type
    return all API call outputs which could lead to the output_type

    Params
    ======
    DefaultDict grouped by semantic type

    """
    def get(self):
        self.bt_explorer = BioThingsExplorer()
        # read in parameters, all parameters are required
        input_prefix = self.get_query_argument('input_prefix')
        input_value = self.get_query_argument('input_value')
        output_prefix = self.get_query_argument('output_prefix')
        max_api = self.get_query_argument('max_api', 2)
        paths = self.bt_explorer.find_path(input_prefix,
                                           output_prefix,
                                           max_no_api_used=int(max_api),
                                           display_graph=False)
        # handle cases where no path could be found to connect from
        # input to output
        if not paths:
            self.set_status(400)
            self.write(json.dumps({"status": 400, "error message": "No paths could be found to connect " + input_prefix + " to " + output_prefix + "using at most " + str(max_api) + " apis!"}))
            self.finish()
        else:
            # for the moment, only select the first path
            # need to be modified to handle multiple paths
            path = paths[0]
            outputs = self.bt_explorer.find_output(path=path,
                                                   input_value=input_value,
                                                   display_graph=False,
                                                   return_networkx=False)
            if outputs:
                self.write(json.dumps({'data': outputs}))
            else:
                self.set_status(400)
                self.write(json.dumps({"status": 400, "error message": "Paths could be located connecting " + input_prefix +
                                   " to " + output_prefix + ". However, no output could be found using the endpoint!"}))
