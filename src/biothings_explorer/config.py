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
        "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/kevin/ID_MAPPING_NEW.csv",
        "file": os.path.join(os.path.dirname(__file__), "openapi_specs/ID_MAPPING_NEW.csv")
    },
    "attribute_mapping": {
        "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/kevin/ATTRIBUTE_LIST.csv",
        "file": os.path.join(os.path.dirname(__file__), "openapi_specs/ATTRIBUTE_LIST.csv")
    }
}

MYGENE_URI2SCOPE = {
    "uniprot": "uniprot.Swiss-Prot",
    "hgnc.symbol": "symbol",
    "hgnc": "hgnc",
    "omim.gene": "MIM",
    "ncbigene": "entrezgene",
    "ensembl.gene": "ensembl.gene",
    "ensembl.protein": "ensembl.protein",
    "ensembl.transcript": "ensembl.transcript"
}

MYCHEM_URI2SCOPE = {
    "inchikey": "pubchem.inchikey",
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

MYGENE_QUERY_JSONLD = dict((y,x) for x,y in MYGENE_URI2SCOPE.items())

MYCHEM_QUERY_JSONLD = dict((y,x) for x,y in MYCHEM_URI2SCOPE.items())