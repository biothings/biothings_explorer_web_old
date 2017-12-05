import yaml
import requests
from bs4 import BeautifulSoup
import csv

template_url = 'https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/master/{api}/openapi_full.yml'
api_list = ['mygene.info', 'myvariant.info', 'mychem.info', 'biolink']

def parse_openapi_yaml(api_name):
    '''parse yaml file and get input/output info for each endpoint

    keyword arguments:
    file_path: the location of the yaml file
    '''
    summary = {'api': '', 'desc': '', 'paths': []}
    url = template_url.replace('{api}', api_name)
    yaml_file = requests.get(url).content
    data = yaml.load(yaml_file)
    summary['api'] = data['info']['title']
    summary['desc'] = data['info']['description']
    paths = data['paths']
    for _path_name, _path_info in paths.items():
        output = [_item['valueType'] for _item in _path_info['get']['responses']['200']['x-responseValueType']]
        path_summary = {'name': _path_name, 
                        'desc': _path_info['get']['parameters'][0]['description'],
                        'input': _path_info['get']['parameters'][0]['x-valueType'],
                        'output': output}
        summary['paths'].append(path_summary)
    return summary



def extract_all_input_output():
    '''This code is used to extract all input/output identifiers from APIs
    for construction of the ID_MAPPING table
    '''
    results = []
    for _api in api_list:
        url = template_url.replace('{api}', _api)
        yaml_file = requests.get(url).content
        data = yaml.load(yaml_file)
        paths = data['paths']
        for _path_name, _path_info in paths.items():
            # add ouput to results
            results += [_item['valueType'] for _item in _path_info['get']['responses']['200']['x-responseValueType']]
            # add input to results
            results += _path_info['get']['parameters'][0]['x-valueType']
    return set(results)

def construct_id_mapping(file_name, ids):
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=['URI', 'Recommended name', 'Registry identifier', 'Alternative name(s)', 'Description', 'Identifier pattern'])
        dict_writer.writeheader()
        info_list = []
        for _id in ids:
            r = requests.get(_id).content
            soup = BeautifulSoup(r, 'lxml')
            table = soup.find('table', attrs={'class': 'collection_item'})
            if table:
                _dict = {'URI': _id}
                rows = table.find_all('tr')
                data = []
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    data.append([ele for ele in cols if ele])
                for info in data:
                    _dict.update({info[0]: info[1]})
                info_list.append(_dict)
                dict_writer.writerow(_dict)
            else:
                info_list.append({'URI': _id})
                dict_writer.writerow({'URI': _id})
    return info_list


