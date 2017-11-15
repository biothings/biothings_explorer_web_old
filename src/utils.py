import re
import yaml
import requests
import csv
import pandas as pd


class SmartAPIHandler:
    def __init__(self):
        # description info about endpoint, bioentity and api
        self.endpoint_info = {}
        self.bioentity_info = {}
        self.api_info = {}
        # path to fetch openapi info
        self.template_url = 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/master/{{api_name}}/openapi_full.yml'
        self.parse_id_mapping()
    '''
    This function parse the openapi yml file, and organize info into endpoints and apis
    '''
    def parse_openapi(self, api_name):
        api_info = {}
        endpoint_info = {}
        openapi_url = self.template_url.replace('{{api_name}}', api_name)
        # check if the openapi file for the api exists first
        if requests.get(openapi_url).status_code == 200:
            # retrieve openapi file
            openapi_file = requests.get(openapi_url).content
            data = yaml.load(openapi_file)
            self.api_info[api_name] = {'info': data['info'], 'servers': data['servers'], 'endpoints': []}
            for _name, _info in data['paths'].items():
                self.endpoint_info[data['servers'][0]['url'] + _name] = _info
                output = [_item['valueType'] for _item in _info['get']['responses']['200']['x-responseValueType']]
                output = [self.bioentity_info[_item] for _item in output]
                _input = [self.bioentity_info[_item] for _item in _info['get']['parameters'][0]['x-valueType']]
                self.endpoint_info[data['servers'][0]['url'] + _name].update({'output': output, 'input': _input})
                self.api_info[api_name]['endpoints'].append(data['servers'][0]['url'] + _name)
            return data

    '''
    construct requests params/data, based on input type and value
    only handle 'in' value which is body or query
    '''
    def api_call_constructor(self, uri, value, endpoint_name):
        results = {}
        method = type(value) == list and 'post' or 'get'
        for _para in self.endpoint_info[endpoint_name][method]['parameters']:
            # handle cases where input value is part of the url
            if _para['in'] == 'path':
                data = requests.get(endpoint_name.replace(_para['name'], value), headers={ "Content-Type" : "application/json"})
                return data
            else:
                # check whether the parameter is required
                if _para['required']:
                    # if the para has a request template, then put value into the placeholder {{input}}
                    if 'x-requestTemplate' in _para:
                        for _template in _para['x-requestTemplate']:
                            if _template['valueType'] == 'default':
                                results[_para['name']] = _template['template'].replace('{{input}}', value)
                            elif uri == _template['valueType']:
                                results[_para['name']] = _template['template'].replace('{{input}}', value)
                    else:
                        results[_para['name']] = value
        print(results)
        if type(value) != list:
            data = requests.get(endpoint_name, params=results)
        else:
            data = requests.post(endpoint_name, data=results)
        return data
  
    '''
    parse the uri_id mapping file, return a dict containing id mapping info indexed by uri
    '''
    def parse_id_mapping(self):
        file_url = 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/master/ID_MAPPING.csv'
        data = pd.read_csv(file_url, encoding = "ISO-8859-1")
        data = data.where((pd.notnull(data)), None)
        for index, row in data.iterrows():
            self.bioentity_info[row['URI']] = {'registry_identifier': row[2], 'alternative_names': row[3], 'description': row[4], 'identifier_pattern': row[-1], 'preferred_name': row[1], 'uri': row['URI']}
        return self.bioentity_info

    '''
    fetch endpoint jsonld contextinformation
    '''
    def fetch_context(self, endpoint_name):
        file_url = self.endpoint_info[endpoint_name]['get']['responses']['200']['x-JSONLDContext']
        return requests.get(file_url).json()




