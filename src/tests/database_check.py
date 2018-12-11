import logging
import requests
import os, sys
import datetime
import json
from bs4 import BeautifulSoup

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import test_log_file, database_status_file

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger_handler = logging.FileHandler(test_log_file, mode='w')
logger_handler.setLevel(logging.DEBUG)
logger_handler.setFormatter(logger_formatter)
logger.addHandler(logger_handler)

class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None

        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)

            if not val:
                break;

        return val

def fetch_api_results(url):
    try:
        response = requests.get(url, headers={'Accept': 'application/json'}).json()
        return response
    except:
        logger.error('%s could not be accessed!', url)


def get_mygene_data_sources():
    """ Get All Data Sources Integrated In MyGene.info
    """
    MYGENE_SOURCE_URL = 'http://mygene.info/v3/metadata'
    mygene_metadata = fetch_api_results(MYGENE_SOURCE_URL)
    results = []
    mygene_sources = DictQuery(mygene_metadata).get('src')
    if mygene_sources:
        for k, v in mygene_sources.items():
            results.append({'source_name': str(k).lower(), 'source_version': DictQuery(v).get('version')})
    if results:
        logger.info('Managed to get data sources integrated in MyGene.info')
    else:
        logger.error('Unable to get data sources for MyGene.info!')
    return results

def get_mychem_data_sources():
    """ Get All Data Sources Integrated in MyChem.info
    """
    MYCHEM_SOURCE_URL = 'http://mychem.info/v1/metadata'
    mychem_metadata = fetch_api_results(MYCHEM_SOURCE_URL)
    results = []
    mychem_sources = DictQuery(mychem_metadata).get('src')
    if mychem_sources:
        for k, v in mychem_sources.items():
            results.append({'source_name': str(k).lower(), 'source_version': DictQuery(v).get('version')})
    if results:
        logger.info('Managed to get data sources integrated in MyChem.info')
    else:
        logger.error('Unable to get data sources for MyChem.info!')
    return results

def get_dgidb_data_sources():
    """ Get All Data Sources Integrated in DGIdb
    """
    DGIDB_SOURCE_URL = 'http://dgidb.org/api/v2/interaction_sources.json'
    dgidb_metadata = fetch_api_results(DGIDB_SOURCE_URL)
    results = []
    if dgidb_metadata:
        results = [{'source_name': str(_item).lower(), 'source_version': None} for _item in dgidb_metadata]
    if results:
        logger.info('Managed to get data sources integrated in DGIdb')
    else:
        logger.error('Unable to get data sources for DGIdb!')
    return results

def get_ebi_ols_data_sources():
    """ Get All Data Sources Integrated in EBI OLS
    """
    EBI_OLS_URL = 'https://www.ebi.ac.uk/ols/api/ontologies?page=0&size=220'
    ols_metadata = fetch_api_results(EBI_OLS_URL)
    results = []
    ols_sources = DictQuery(ols_metadata).get('_embedded/ontologies')
    if ols_sources:
        for k in ols_sources:
            results.append({'source_name': str(DictQuery(k).get('ontologyId')).lower(), 'source_version': DictQuery(k).get('updated')})
    if results:
        logger.info('Managed to get data sources integrated in EBI OLS')
    else:
        logger.error('Unable to get data sources for EBI OLS!')
    return results

def get_chembl_data_sources():
    """ Get All Data Sources Integrated in ChEMBL
    """
    CHEMBL_URL = 'https://www.ebi.ac.uk/chembl/api/data/source?limit=100'
    chembl_metadata = fetch_api_results(CHEMBL_URL)
    results = []
    if chembl_metadata:
        chembl_sources = DictQuery(chembl_metadata).get('sources')
    if chembl_sources:
        results = [{'source_name': str(DictQuery(k).get('src_description')).lower(), 'source_version': None} for k in chembl_sources if DictQuery(k).get('src_description')!= 'Undefined']
    if results:
        logger.info('Managed to get data sources integrated in ChEMBL')
    else:
        logger.error('Unable to get data sources for ChEMBL!')
    return results

def get_biolink_sources():
    """ Get All Data Sources Integrated in BioLink
    """
    BIOLINK_URL = 'https://monarchinitiative.org/about/sources'
    doc = requests.get(BIOLINK_URL)
    results = []
    soup = BeautifulSoup(doc.content)
    table = soup.find('div', attrs={'class': 'content'})
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        if cols:
            source_info = cols[1].find_all('b')[0].contents[0]
            results.append({'source_name': source_info.lower(), 'source_version': cols[-1].contents[0]})
    if results:
        logger.info('Managed to get data sources integrated in BioLink')
    else:
        logger.error('Unable to get data sources for BioLink!')
    return results

def get_pharos_sources():
    """ Get All Data Sources Integrated in Pharos
    """
    PHAROS_URL = 'https://pharos.nih.gov/idg/help'
    doc = requests.get(PHAROS_URL)
    results = []
    soup = BeautifulSoup(doc.content)
    table = soup.find('table', attrs={'class': 'table-striped'})
    rows = table.findAll('tr')
    for tr in rows:
        cols = tr.findAll('td')
        if cols:
            source_info = cols[0].contents[0]
            try:
                source_info = source_info.contents[0]
            except:
                continue
            results.append({'source_name': source_info, 'source_version': None})
    if results:
        logger.info('Managed to get data sources integrated in BioLink')
    else:
        logger.error('Unable to get data sources for BioLink!')
    return results

def get_pubchem_sources():
    """ Get All Data Sources Integrated in PubChem
    """
    PUBCHEM_URL = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/sourcetable/substance/JSON'
    pubchem_metadata = fetch_api_results(PUBCHEM_URL)
    results = []
    if pubchem_metadata:
        pubchem_sources = DictQuery(pubchem_metadata).get('Table/Row')
    if pubchem_sources:
        results = [{'source_name': _doc['Cell'][0], 'source_version': _doc['Cell'][-1]} for _doc in pubchem_sources]
    if results:
        logger.info('Managed to get data sources integrated in PubChem')
    else:
        logger.error('Unable to get data sources for PubChem!')
    return results

def get_mydisease_sources():
    """ Get All Data Sources Integrated in MyDisease.info
    """
    results = [{'source_name': 'ctd', 'source_version': '2018.6'}, {'source_name': 'hpo', 'source_version': '2018.6'},
               {'source_name': 'disgenet', 'source_version': '2018.6'}, {'source_name': 'mondo', 'source_version': '2018.6'}]
    logger.info('Managed to get data sources integrated in MyDisease.info')
    return results

def get_reactome_sources():
    """ Get All Data Sources Integrated in Reactome
    """
    now = datetime.datetime.now()
    results = [{'source_name': 'reactome', 'source_version': str(now.year) + '.' + str(now.month)}]
    logger.info('Managed to get data sources integrated in Reactome')
    return results

def get_taxonomy_sources():
    """ Get All Data Sources Integrated in t.biothings.io
    """
    now = datetime.datetime.now()
    results = [{'source_name': 'ncbi taxonomy', 'source_version': str(now.year) + '.' + str(now.month)}]
    logger.info('Managed to get data sources integrated in Taxonomy API')
    return results

def get_disease_ontology_sources():
    """ Get All Data Sources Integrated in Disease Ontology API
    """
    now = datetime.datetime.now()
    results = [{'source_name': 'disease ontology', 'source_version': str(now.year) + '.' + str(now.month)}]
    logger.info('Managed to get data sources integrated in Disease Ontology API')
    return results

def get_hgnc_sources():
    """ Get All Data Sources Integrated in HGNC API
    """
    now = datetime.datetime.now()
    results = [{'source_name': 'hgnc', 'source_version': str(now.year) + '.' + str(now.month)}]
    logger.info('Managed to get data sources integrated in HGNC API')
    return results

if __name__ == "__main__":
    results = {'timestamp': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p"),
               'status': {
                   'BioLink API': get_biolink_sources(),
                   'ChEMBL API': get_chembl_data_sources(),
                   'DGIdb API': get_dgidb_data_sources(),
                   'Disease Ontology API': get_disease_ontology_sources(),
                   'EBI Ontology Service API': get_ebi_ols_data_sources(),
                   'HGNC API': get_hgnc_sources(),
                   'MyChem.info API': get_mychem_data_sources(),
                   'MyDisease.info API': get_mydisease_sources(),
                   'MyGene.info API': get_mygene_data_sources(),
                   'Pharos API': get_pharos_sources(),
                   'PubChem API': get_pubchem_sources(),
                   'Reactome API': get_reactome_sources(),
                   'Taxonomy API': get_taxonomy_sources()
                }
            }
    with open(database_status_file, 'w') as outfile:
        json.dump(results, outfile)
    logger.info('Loaded all database status!')
