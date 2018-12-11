import requests
import os, sys
import json
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

API_CALLS = {
    "MyGene.info": "http://mygene.info/v3/gene/1017",
    "MyChem.info": "http://mychem.info/v1/query?q=drugbank.name:riluzole",
    "MyDisease.info": "http://mydisease.info/v1/disease/MONDO:0013632",
    "Reactome": "https://reactome.org/ContentService/data/pathway/R-HSA-5673001/containedEvents",
    "DGIdb": "http://www.dgidb.org/api/v2/interactions.json?genes=CXCR4",
    "BioLink": "https://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:4750/phenotypes/",
    "Disease Ontology": "http://www.disease-ontology.org/api/metadata/DOID%3A162/",
    "Pharos": "https://pharos.nih.gov/idg/api/v1/targets(1)?view=full&format=jsonld",
    "EBI OLS": "https://www.ebi.ac.uk/ols/api/ontologies/doid/terms/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FDOID_11712",
    "ChEMBL": "https://www.ebi.ac.uk/chembl/api/data/target_prediction?molecule_chembl_id__exact=CHEMBL744",
    "PubChem": "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/riluzole/synonyms/JSON",
    "Taxonomy": "http://t.biothings.io/v1/taxon/9090",
    "HGNC": "https://rest.genenames.org/fetch/symbol/CXCR4"
}

from config import api_status_file

def check_api_status(url):
    response = requests.get(url)
    if response.ok:
        return 'O.K.'
    else:
        return 'Failed!'

if __name__ == "__main__":
    status_dict = {'status': {}, 'timestamp': datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")}
    for k,v in API_CALLS.items():
        status_dict['status'][k] = check_api_status(v)
    with open(api_status_file, 'w') as outfile:
        json.dump(status_dict, outfile)
