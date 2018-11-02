import pkg_resources
import os.path

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
        "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/kevin/ID_MAPPING_NEW.csv",
        "file": os.path.join(os.path.dirname(__file__), "openapi_specs/ID_MAPPING_NEW.csv")
    },
    "attribute_mapping": {
        "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/kevin/ATTRIBUTE_LIST.csv",
        "file": os.path.join(os.path.dirname(__file__), "openapi_specs/ATTRIBUTE_LIST.csv")
    }
}

