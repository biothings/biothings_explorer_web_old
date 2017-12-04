import json
import yaml
import pandas as pd
import requests
from pathlib import Path

def int2str(d):
    """
    Iterrative function
    Convert all integer values in the dictionary/JSON to string


    Params
    ======
    d: (dict)
        dictionary to perform int2str function
    """
    for k, v in d.items():
        if isinstance(v, dict):
            int2str(v)
        elif isinstance(v, list):
            for _v in v:
                if isinstance(_v, dict):
                    int2str(_v)
        else:
            if type(v) == int:
                d.update({k: str(v)})

def readFile(file_path):
    """
    Given a file_path, return the file in json/xml/csv
    format based on the suffix

    Params
    ======
    file_path: (str)
        The file path could be a URL or a local file path
        The suffix of the path could be in csv or json or yaml
    """

    # First check if the url or local file path is valid
    # if url/local file is invalid, return empty
    if file_path.startswith('http'):
        status = requests.get(file_path).status_code
        if status == 200:
            data = requests.get(file_path).content
        else:
            print('The url "{}" is invalid!!!! Please double check!'.format(file_path))
            return
    else:
        if Path(file_path).is_file() and not file_path.endswith('csv'):
            with open(file_path) as f:
                data = f.read()
        elif not file_path.endswith('csv'):
            print('The local file path "{}" is invalid!!! Please double check!'.format(file_path))
            return
    # handle csv file using pandas module
    if file_path.endswith('csv'):
        return pd.read_csv(file_path, encoding="ISO-8859-1")
    # handle yaml file using yaml module
    elif file_path.endswith('yml') or file_path.endswith('yaml'):
        return yaml.load(data)
    # handle json file using json module
    elif file_path.endswith('json'):
        if file_path.startswith('http'):
            return json.loads(data.decode())
        else:
            return json.loads(data)
    else:
        print("readFile function could not handle file format other than csv, yml or json!")

def str2list(_input):
    """
    This function takes an input, and determine its type
    if the type is list, return the input without modification
    if the ytpe is string, turn it into list and return

    Params
    ======
    _input: (str or list)
        input to the modification
    """
    if type(_input) == list:
        return _input
    else:
        return [_input]

def output2input(_output):
    """
    This function modifies the output,
    so that it could be consumed as input for another path

    Params
    ======
    _output: (list)
        output to be modified

    Return
    ======
    list of ids
    """
    result = []
    for _iopair in _output:
        output_list = _iopair['output'][0]
        result.extend([_o[0] for _o in output_list])
    return result

