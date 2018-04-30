import json

from biothings_explorer.id_converter import IDConverter
from biothings_explorer.api_registry_parser import RegistryParser
from .basehandler import BaseHandler

class SynonymHandler(BaseHandler):
    """
    This function takes a CURIE, and return all its synonyms
	currently it only handle cases for converting gene and chemical synonyms
	later on will expand it to more semantic types, e.g. disease, phenotype
    Params
    ======
    DefaultDict grouped by semantic type

    """
    def get(self):
        input_prefix = self.get_query_argument('input_prefix')
        input_value = self.get_query_argument('input_value')
        group = self.get_query_argument('group_by_prefix', False)
        registry = RegistryParser(readmethod='filepath', initialize=True)
        converter = IDConverter()
        input_semantic_type = registry.prefix2semantictype(input_prefix)
        if input_semantic_type == 'gene':
            synonyms = converter.find_gene_synonym(input_value, input_prefix)[0]
        elif input_semantic_type == 'chemical':
            synonyms = converter.find_chemical_synonym(input_value, input_prefix)[0]
        else:
            synonyms = {input_prefix: input_value}
        if not group:
            curie_synonyms = []
            for k, v in synonyms.items():
                if type(v) == list:
                    for _v in v:
                        curie = k + ':' + str(_v)
                        curie_synonyms.append(curie)
                else:
                    curie = k + ':' + str(v)
                    curie_synonyms.append(curie)
            self.write(json.dumps({'synonyms': curie_synonyms}))
        else:
            self.write(json.dumps({'synonyms': synonyms}))
