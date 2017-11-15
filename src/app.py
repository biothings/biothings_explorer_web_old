
import logging
import tornado.auth
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import uuid
import json
import pprint
from  tornado.escape import json_decode
from  tornado.escape import json_encode
from tornado.options import define, options
import requests
import yaml
from utils import SmartAPIHandler
from jsonld_processor import jsonld2nquads, fetchvalue 

api_names = ['mygene.info', 'myvariant.info', 'mychem.info', 'biolink', 'dgidb', 'proteins api', 'ensembl']
template_url = 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/master/{api}/openapi_full.yml'

# initialize
t = SmartAPIHandler()
for _api in api_names:
    t.parse_openapi(_api)


def parse_openapi_yaml(api_name):
    '''parse yaml file and get input/output info for each endpoint

    keyword arguments:
    file_path: the location of the yaml file
    '''
    t= SmartAPIHandler()
    t.parse_id_mapping()
    summary = {'api': '', 'description': '', 'paths': []}
    url = template_url.replace('{api}', api_name)
    yaml_file = requests.get(url).content
    data = yaml.load(yaml_file)
    print(data)
    summary['api'] = data['info']['title']
    summary['description'] = data['info']['description']
    paths = data['paths']
    for _path_name, _path_info in paths.items():
        output = [_item['valueType'] for _item in _path_info['get']['responses']['200']['x-responseValueType']]
        output = [t.bioentity_info[_item] for _item in output]
        _input = [t.bioentity_info[_item] for _item in _path_info['get']['parameters'][0]['x-valueType']]
        path_summary = {'name': data['servers'][0]['url'] + _path_name,
                        'description': _path_info['get']['summary'],
                        'input': _input,
                        'output': output}
        summary['paths'].append(path_summary)
    return summary

def relation_handler():
    api_list = []
    for _api_name in api_names:
        api_list.append(parse_openapi_yaml(_api_name))
    return api_list

def path_handler(path, value, level):
    # get all meta data informaiton ready
    result = []
    t = SmartAPIHandler()
    for _api_name in api_names:
        t.parse_openapi(_api_name)
    t.parse_id_mapping()
    # convert id name to uri
    for k, v in t.bioentity_info.items():
        if v['preferred_name'] == path['input']:
            _input = k
        elif v['preferred_name'] == path['output']:
            _output = k
    value = value.split(',')
    # make api call with input and endpoint name
    for _value in value:
        json_doc = t.api_call_constructor(_input, _value, path['endpoint']).json()
        # construct jsonld doc
        jsonld_context = t.fetch_context(path['endpoint'])
        json_doc.update(jsonld_context)
        # parse output nquads
        nquads = jsonld2nquads(json_doc)
        pprint.pprint(nquads)
        pprint.pprint(_output)
        outputs = list(set(fetchvalue(nquads, _output)))
        pprint.pprint(outputs)
        for output in outputs:
            result.append([_value, output, level])
    return result


class MainHandler(tornado.web.RequestHandler):
    @tornado.web.addslash
    def get(self):
        self.render("index.html", messages=None)

class PathHandler(tornado.web.RequestHandler):

    def post(self):
        json_obj = json_decode(self.request.body)
        response_to_send = []
        if len(json_obj['path']) == 1:
            pprint.pprint(json_obj)
            response_to_send = path_handler(json_obj['path'][0], json_obj['input'], 0)
        else:
            _input = json_obj['input']
            for i, _path in enumerate(json_obj['path']):
                response = path_handler(_path, _input, i)
                response_to_send += response
                _input = [_response[1] for _response in response]
                _input = ','.join(_input)
        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))


class RelationHandler(tornado.web.RequestHandler):

    def post(self):
        response_to_send = {'api': t.api_info, 'endpoint': t.endpoint_info, 'bioentity': t.bioentity_info}
        pprint.pprint(response_to_send)
        self.write(json.dumps(response_to_send))


class Application(tornado.web.Application):

    def __init__(self):
        settings = {
            'debug': True,
            'template_path': os.path.join(os.path.dirname(__file__), "templates"),
            'static_path': os.path.join(os.path.dirname(__file__), "static")
        }
        handlers = [
            (r"/explorer/?", MainHandler),
            (r"/explorer/static/(.*)", tornado.web.StaticFileHandler, {'path': settings['static_path']}),
            (r"/explorer/relation/", RelationHandler),
            (r"/explorer/path/", PathHandler)
        ]

        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    app = Application()
    app.listen(8853)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
