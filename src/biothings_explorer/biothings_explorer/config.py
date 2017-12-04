import pkg_resources
import os.path
import requests

BUILDIN_CONTEXT_PATH = pkg_resources.resource_filename('biothings_explorer', 'openapi_specs')

FILE_PATHS = {
    "registry_repo": {
        "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/master/",
        "file": os.path.join(os.path.dirname(__file__), "openapi_specs")
    },
    "api_list": {
        "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/kevin/API_LIST.yml",
        "file": os.path.join(os.path.dirname(__file__), "openapi_specs/API_LIST.yml")
    },
    "id_mapping": {
        "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/kevin/ID_MAPPING.csv",
        "file": os.path.join(os.path.dirname(__file__), "openapi_specs/ID_MAPPING.csv")
    }
}
