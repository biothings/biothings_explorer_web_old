import requests
from pyld import jsonld

from .config import MYGENE_URI2SCOPE, MYCHEM_URI2SCOPE, MYGENE_QUERY_JSONLD, MYCHEM_QUERY_JSONLD

class IDConverter:
    def __init__(self):
        self.mygene_params_template = 'q={input_value}&scopes={input_type}&fields=symbol,entrezgene,MIM,uniprot.Swiss-Prot,ensembl.gene,ensembl.protein,ensembl.transcript&dotfield=True'
        self.mychem_params_template = 'q={input_value}&scopes={input_type}&fields=drugbank.name,pubchem.inchikey,aeolus.drug_rxcui,chembl.chebi_par_id,chembl.molecule_chembl_id,drugbank.drugbank_id,drugbank.iuphar,drugbank.kegg_drug,drugbank.kegg_compound,drugbank.pubchem_compound,unii.unii,chebi.inchi&dotfield=True'
        self.mygene_url = 'http://mygene.info/v3/query'
        self.mychem_url = 'http://mychem.info/v1/query'
        self.header = {'content-type': 'application/x-www-form-urlencoded'}

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
        params = self.mygene_params_template.replace('{input_value}', str(input_value)).replace('{input_type}', MYGENE_URI2SCOPE[input_type])
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
        mygene_docs = requests.post(self.mygene_url, params=params, headers=self.header).json()
        mygene_flatten = []
        for _doc in mygene_docs:
            mygene_jsonld_doc = {}
            for k,v in _doc.items():
                if k in MYGENE_QUERY_JSONLD:
                    mygene_jsonld_doc[MYGENE_QUERY_JSONLD[k]] = v
            mygene_flatten.append(mygene_jsonld_doc)
        return mygene_flatten

    def convert_gene_ids(self, input_value, input_type, target_type):
        synonyms = self.find_gene_synonym(input_value, input_type)
        for _synonym in synonyms:
            if target_type in _synonym:
                yield _synonym[target_type]
            else:
                yield None

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
