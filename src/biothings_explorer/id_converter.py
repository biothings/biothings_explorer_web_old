import requests
from collections import defaultdict

from .api_registry_parser import RegistryParser
from .utils import autolog

import logging
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import id_converter_log_file

# logging module
logger = logging.getLogger('id_converter')
logger.setLevel(logging.DEBUG)
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_handler = logging.FileHandler(id_converter_log_file)
logger_handler.setLevel(logging.DEBUG)
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

##########################################################
MYGENE_FIELDNAME2QUERYNAME = {
    "uniprot": "uniprot",
    "hgnc.symbol": "symbol",
    "hgnc": "hgnc",
    "omim.gene": "MIM",
    "ncbigene": "entrezgene",
    "ensembl.gene": "ensembl.gene",
    "ensembl.protein": "ensembl.protein",
    "ensembl.transcript": "ensembl.transcript"
}

MYCHEM_URI2SCOPE = {
    "inchikey": "_id",
    "rxcui": "aeolus.drug_rxcui",
    "chebi": "chembl.chebi_par_id",
    "chembl.compound": "chembl.molecule_chembl_id",
    "drugbank": "drugbank.drugbank_id",
    "iuphar.ligand": "drugbank.iuphar",
    "kegg.drug": "drugbank.kegg_drug",
    "kegg.compound": "drugbank.kegg_compound",
    "pubchem.compound": "drugbank.pubchem_compound",
    "unii": "unii.unii",
    "inchi": "chebi.inchi",
    "drugname": "drugbank.name"
}

MYDISEASE_URI2SCOPE = {
    "doid": "mondo.xrefs.doid",
    "omim.disease": "mondo.xrefs.omim",
    "umls.disease": "mondo.xrefs.umls",
    "mondo": "_id"
}

MYGENE_QUERY_JSONLD = dict((y,x) for x,y in MYGENE_FIELDNAME2QUERYNAME.items())
MYGENE_QUERY_JSONLD['uniprot.Swiss-Prot'] = "uniprot"
MYDISEASE_QUERY_JSONLD = dict((y,x) for x,y in MYDISEASE_URI2SCOPE.items())
MYCHEM_QUERY_JSONLD = dict((y,x) for x,y in MYCHEM_URI2SCOPE.items())
##########################################################

class IDConverter:
    def __init__(self):
        self.mygene_params_template = 'q={input_value}&scopes={input_type}&fields=symbol,entrezgene,MIM,uniprot.Swiss-Prot,ensembl.gene&dotfield=True&species=human'
        self.mychem_params_template = 'q={input_value}&scopes={input_type}&fields=drugbank.name,pubchem.inchi_key,aeolus.drug_rxcui,chembl.chebi_par_id,chembl.molecule_chembl_id,drugbank.drugbank_id,drugbank.iuphar,drugbank.kegg_drug,drugbank.kegg_compound,drugbank.pubchem_compound,unii.unii,chebi.inchi&dotfield=True'
        self.mydisease_params_template = 'q={input_value}&scopes={input_type}&fields=mondo.xrefs&dotfield=true'
        self.mygene_url = 'http://mygene.info/v3/query'
        self.mychem_url = 'http://mychem.info/v1/query'
        self.mydisease_url = 'http://mydisease.info/v1/query'
        self.header = {'content-type': 'application/x-www-form-urlencoded'}
        self.registry = RegistryParser(readmethod='filepath', initialize=True)

    def group_curies_by_prefix(self, curie_list):
        id_group = defaultdict(list)
        for _curie in curie_list:
            _prefix = _curie.split(':')[0].lower()
            id_group[_prefix].append(_curie[len(_prefix)+1:])
        return id_group

    def find_synonym(self, input_value, input_type):
        """find synonym of given input
        This is wrapper function for find_gene_synonym, find_chemical_synonym, find_disease_synonym
        """
        semantic_type = self.registry.prefix2semantictype(input_type)
        if semantic_type == 'gene':
            return self.find_gene_synonym(input_value, input_type)
        elif semantic_type == 'chemical':
            return self.find_chemical_synonym(input_value, input_type)
        elif semantic_type == 'disease':
            return self.find_disease_synonym(input_value, input_type)
        else:
            return [{input_type: input_value}]
    
    def find_gene_synonym(self, input_value, input_type):
        """
        Input: "ncbigene:1017",
        output: {
                    "http://identifiers.org/hgnc/": "1771",
                    "http://identifiers.org/ensembl.gene/": "ENSG00000123374",
                    "http://identifiers.org/hgnc.symbol/": "CDK2",
                    "http://identifiers.org/uniprot": "P24941"
                }
        """
        # check whether the input_type is within MYGENE_FIELDNAME2QUERYNAME
        try:
            params = self.mygene_params_template.replace('{input_value}', str(input_value)).replace('{input_type}', MYGENE_FIELDNAME2QUERYNAME[input_type])
        except KeyError:
            error_message = input_type + ' is not in MYGENE_FIELDNAME2QUERYNAME'
            autolog(logger, error_message, 'warn')
            return
        # make requests to mygene
        mygene_docs = requests.post(self.mygene_url, params=params, headers=self.header).json()
        mygene_flatten = []
        for _doc in mygene_docs:
            # 
            if 'notfound' in _doc and _doc['notfound'] == True:
                error_message = 'The input is invalid: ' + input_type + ':' + _doc['query']
                autolog(logger, error_message, 'warn')
            mygene_jsonld_doc = {}
            for k,v in _doc.items():
                if k in MYGENE_QUERY_JSONLD:
                    mygene_jsonld_doc[MYGENE_QUERY_JSONLD[k]] = v
            mygene_flatten.append(mygene_jsonld_doc)
        if mygene_flatten == [{}]:
            return
        else:
            return mygene_flatten

    def convert_gene_ids(self, input_value, input_type, target_type):
        """
        
        """
        synonyms = self.find_gene_synonym(input_value, input_type)
        if synonyms:
            for _synonym in synonyms:
                if target_type in _synonym:
                    yield _synonym[target_type]
                else:
                    yield None
        else:
            yield None

    def convert_gene_ids_in_batch(self, input_value, input_type, target_type):
        synonyms = self.find_gene_synonym(input_value, input_type)
        results = defaultdict(list)
        for _synonym in synonyms:
            if target_type in _synonym:
                _input = str(_synonym[input_type]).upper()
                results[_input].append(_synonym[target_type])
        return results

    def convert_gene_ids_in_curies_in_batch(self, curie_list, target_type):
        final_results = {}
        id_group = self.group_curies_by_prefix(curie_list)
        for k, v in id_group.items():
            input_values = ','.join(v)
            temp_result = self.convert_gene_ids_in_batch(input_values, k, target_type)
            final_results.update(temp_result)
        return final_results

    def find_disease_synonym(self, input_value, input_type):
        """
        Input: "ncbigene:1017",
        output: {
                    "http://identifiers.org/hgnc/": "1771",
                    "http://identifiers.org/ensembl.gene/": "ENSG00000123374",
                    "http://identifiers.org/hgnc.symbol/": "CDK2",
                    "http://identifiers.org/uniprot": "P24941"
                }
        """
        input_value = str(input_value)
        if input_type == "mondo" and "MONDO" not in input_value.upper():
            input_value = "MONDO:" + input_value
        if input_type == "doid" and "DOID" not in input_value.upper():
            input_value = "DOID:" + input_value

        params = self.mydisease_params_template.replace('{input_value}', str(input_value)).replace('{input_type}', MYDISEASE_URI2SCOPE[input_type])
        """
        if mode == 'single':
            # check whether input_value is single
            # check whether input_type is uri and whether is in the URI2SCOPE dict            
            # get json doc from mygene.info
            mygene_doc = requests.get(self.mygene_url, params=params).json()['hits'][0]
            # add jsonld context file
            mygene_jsonld_doc = {}
            for k,v in mygene_doc.items():
                if k in MYGENE_QUERY_JSONLD:
                    mygene_jsonld_doc[MYGENE_QUERY_JSONLD[k]] = v
            return mygene_jsonld_doc
        else:
            """
        mydisease_docs = requests.post(self.mydisease_url, params=params, headers=self.header).json()
        mydisease_flatten = []
        for _doc in mydisease_docs:
            mydisease_jsonld_doc = {}
            for k,v in _doc.items():
                if k in MYDISEASE_QUERY_JSONLD:
                    mydisease_jsonld_doc[MYDISEASE_QUERY_JSONLD[k]] = v.split(':')[-1]
            mydisease_flatten.append(mydisease_jsonld_doc)
        return mydisease_flatten

    def convert_disease_ids(self, input_value, input_type, target_type):
        synonyms = self.find_disease_synonym(input_value, input_type)
        for _synonym in synonyms:
            if target_type in _synonym:
                yield _synonym[target_type]
            else:
                yield None

    def convert_disease_ids_in_batch(self, input_value, input_type, target_type):
        synonyms = self.find_disease_synonym(input_value, input_type)
        results = defaultdict(list)
        for _synonym in synonyms:
            if target_type in _synonym:
                _input = str(_synonym[input_type]).split(':')[1].upper()
                results[_input].append(_synonym[target_type])
        return results

    def convert_disease_ids_in_curies_in_batch(self, curie_list, target_type):
        final_results = {}
        id_group = self.group_curies_by_prefix(curie_list)
        for k, v in id_group.items():
            input_values = ','.join(v)
            temp_result = self.convert_disease_ids_in_batch(input_values, k, target_type)
            final_results.update(temp_result)
        return final_results

    def find_chemical_synonym(self, input_value, input_type):
        """
        Input: "ncbigene:1017",
        output: {
                    "http://identifiers.org/hgnc/": "1771",
                    "http://identifiers.org/ensembl.gene/": "ENSG00000123374",
                    "http://identifiers.org/hgnc.symbol/": "CDK2",
                    "http://identifiers.org/uniprot": "P24941"
                }
        """
        params = self.mychem_params_template.replace('{input_value}', str(input_value)).replace('{input_type}', MYCHEM_URI2SCOPE[input_type])
        """
        if mode == 'single':
            # check whether input_value is single
            # check whether input_type is uri and whether is in the URI2SCOPE dict            
            # get json doc from mygene.info
            mychem_doc = requests.get(self.mychem_url, params=params).json()['hits'][0]
            # add jsonld context file
            mychem_jsonld_doc = {}
            for k,v in mychem_doc.items():
                if k in MYCHEM_QUERY_JSONLD:
                    mychem_jsonld_doc[MYCHEM_QUERY_JSONLD[k]] = v
            return mychem_jsonld_doc
        else:
            """
        mychem_docs = requests.post(self.mychem_url, params=params, headers=self.header).json()
        mychem_flatten = []
        for _doc in mychem_docs:
            mychem_jsonld_doc = {}
            for k,v in _doc.items():
                if k in MYCHEM_QUERY_JSONLD:
                    mychem_jsonld_doc[MYCHEM_QUERY_JSONLD[k]] = v
            mychem_flatten.append(mychem_jsonld_doc)
        return mychem_flatten

    def convert_chemical_ids(self, input_value, input_type, target_type):
        synonyms = self.find_chemical_synonym(input_value, input_type)
        for _synonym in synonyms:
            if target_type in _synonym:
                yield _synonym[target_type]
            else:
                yield None

    def convert_chemical_ids_in_batch(self, input_value, input_type, target_type):
        synonyms = self.find_chemical_synonym(input_value, input_type)
        results = defaultdict(list)
        for _synonym in synonyms:
            if target_type in _synonym:
                _input = str(_synonym[input_type]).upper()
                results[_input].append(_synonym[target_type])
        return results

    def convert_chemical_ids_in_curies_in_batch(self, curie_list, target_type):
        final_results = {}
        id_group = self.group_curies_by_prefix(curie_list)
        for k, v in id_group.items():
            input_values = ','.join(v)
            temp_result = self.convert_chemical_ids_in_batch(input_values, k, target_type)
            final_results.update(temp_result)
        return final_results
