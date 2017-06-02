import pkg_resources
import os.path
import requests

BUILDIN_CONTEXT_PATH = pkg_resources.resource_filename('biothings_explorer', 'context')

AVAILABLE_IDS = {
    "ensembl_gene_id": {
        "uri": "http://identifiers.org/ensembl.gene/",
        "example": "ENSG00000139618"
    },
    "ensembl_protein_id": {
        "uri": "http://identifiers.org/ensembl.protein/",
        "example": "ENSP0000012345"
    },
    "ensembl_transcript_id": {
        "uri": "http://identifiers.org/ensembl.transcript/",
        "example": "ENST0000012345"
    },
    "gene_ontology_id": {
        "uri": "http://identifiers.org/go/",
        "example": "GO:1234556"
    },
    "interpro_id": {
        "uri": "http://identifiers.org/interpro/",
        "example": "interpro"
    },
    "refseq_id": {
        "uri": "http://identifiers.org/refseq/",
        "example": "refseq"
    },
    "sympdb_id": {
        "uri": "http://identifiers.org/sympdb/",
        "example": "sympdb"
    },
    "reactome_id": {
        "uri": "http://identifiers.org/reactome/",
        "example": "reactome"
    },
    "pharmgkb_pathway_id": {
        "uri": "http://identifiers.org/pharmgkb.pathways/",
        "example": "pharmgkb"
    },
    "kegg_pathway_id": {
        "uri": "http://identifiers.org/kegg.pathway/",
        "example": "kegg"
    },
    "biocarta_id": {
        "uri": "http://identifiers.org/biocarta.pathway/",
        "example": "biocarta"
    },
    "entrez_gene_id": {
        "uri": "http://identifiers.org/hgnc/",
        "example": 1017
    },
    "hgnc_gene_symbol": {
        "uri": "http://identifiers.org/hgnc.symbol/",
        "example": "CDK7"
    },
    "hgvs_id": {
        "uri": "http://identifiers.org/hgvs/",
        "example": "chr6:123456G>A"
    },
    "dbsnp_id": {
        "uri": "http://identifiers.org/dbsnp/",
        "example": "rs123456"
    },
    "drugbank_id": {
        "uri": "http://identifiers.org/drugbank/",
        "example": "DB00002"
    },
    "drug_symbol": {
        "uri": "http://identifiers.org/drug.symbol/",
        "example": "SUNITINIB"
    },
    "pubchem_id": {
        "uri": "http://identifiers.org/pubchem.compound/",
        "example": 100101
    },
    "pubmed_id": {
        "uri": "http://identifiers.org/pubmed/",
        "example": 16333295
    },
    "uniprot_id": {
        "uri": "http://identifiers.org/uniprot/",
        "example": "P62158"
    },
    "wikipathway_id": {
        "uri": "http://identifiers.org/wikipathways/",
        "example": "WP100"
    },
    "clinicaltrial_id": {
        "uri": "http://identifiers.org/clinicaltrials/",
        "example": "NCT01314001"
    },
    "symptom": {
        "uri": "http://identifiers.org/symptom/",
        "example": "Microcephanly"
    },
    "diseaseontology_id": {
        "uri": "http://identifiers.org/disease_ontology/",
        "example": "DOID:1089"
    },
    "disease_name": {
        "uri": "http://identifiers.org/disease_name/",
        "example": "Intellectual disability"
    },
    "reactome_id": {
        "uri": "http://identifiers.org/reactome/",
        "example": "R-HSA-199420"
    },
    "pathway_name": {
        "uri": "http://identifiers.org/pathway.name",
        "example": "Deubiquitination"
    },
    "drug_effect": {
        "uri": "http://identifiers.org/drug_effect/",
        "example": "Renal impairment"
    },
    "pharmacology_class": {
        "uri": "http://identifiers.org/pharm_class/",
        "example": "Nonsteroidal Anti-inflammatory Compounds [Chemical/Ingredient]"
    },
    "omim_term": {
        "uri": "http://identifiers.org/omim_term/",
        "example": "Myelokathexis"
    },
    "chembl_id": {
        "uri": "http://identifiers.org/chembl.compound/",
        "example": "CHEMBL1949675"
    },
    "pdb_id": {
        "uri": "http://identifiers.org/pdb/",
        "example": "2K03"
    },
    "mgi_term": {
        "uri": "http://identifiers.org/mgi_term/",
        "example": "endocrine/exocrine gland phenotype"
    },
    "mouse_gene_id": {
        "uri": "http://identifiers.org/mgi/",
        "example": 1860276
    },
    "civic_gene_id": {
        "uri": "http://identifiers.org/civic_gene/",
        "example": 6
    },
    "civic_variant_id": {
        "uri": "http://identifiers.org/civic_variant/",
        "example": 6
    },
    "civic_evidence_id": {
        "uri": "http://identifiers.org/civic_evidence/",
        "example": 6
    },
    "so_id": {
        "uri": "http://identifiers.org/so/",
        "example": "SO:0001121"
    },
    "rxcui": {
        "uri": "http://identifiers.org/rxcui/",
        "example": '603952'
    }
}

AVAILABLE_API_SOURCES = {
    "mygene.info": {
        "annotate_ids": ["entrez_gene_id", "ensembl_gene_id"],
        "query_ids": ["uniprot_id", "ensembl_gene_id", "ensembl_protein_id", "ensembl_transcript_id", "gene_ontology_id", "hgnc_gene_symbol",
                      "wikipathway_id", "interpro_id", "pubmed_id", "biocarta_id", "reactome_id", "refseq_id", "sympdb_id", "pharmgkb_pathway_id",
                      "kegg_pathway_id"],
        "annotate_syntax": "http://mygene.info/v3/gene/*",
        "query_syntax": "http://mygene.info/v3/query?q=*",
        "description": "gene annotation service",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/mygene_context.json")
        }
    },
    "myvariant.info": {
        "annotate_ids": ["hgvs_id"],
        "query_ids": ["entrez_gene_id", "hgnc_gene_symbol", "ensembl_gene_id", "dbsnp_id", "pubmed_id", "uniprot_id"],
        "annotate_syntax": "http://myvariant.info/v1/variant/*",
        "query_syntax": "http://myvariant.info/v1/query?q=*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/myvariant_context.json")
        }
    },
    "mydrug.info": {
        "annotate_ids": ["drugbank_id"],
        "query_ids": ["dbsnp_id", "pubchem_id", "drugbank_id", "rxcui", "drug_symbol", "pubmed_id", "hgnc_gene_symbol", "uniprot_id", "clinicaltrial_id"],
        "annotate_syntax": "http://c.biothings.io/v1/drug/*",
        "query_syntax": "http://c.biothings.io/v1/query?q=*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/mydrug_context.json")
        }
    },
    "dgidb": {
        "annotate_ids": ["hgnc_gene_symbol"],
        "query_ids": ["drug_symbol"],
        "annotate_syntax": "http://localhost:8899/dgidb/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/dgidb_context.json")
        }
    },
    "lynx_symptoms": {
        "annotate_ids": ["hgnc_gene_symbol"],
        "query_ids": ["entrez_gene_id", "symptom"],
        "annotate_syntax": "http://lynx.ci.uchicago.edu/gediresources/resources/genes/9606/*/symptoms",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/lynx_symptom_context.json")
        }
    },
    "lynx_disease": {
        "annotate_ids": ["hgnc_gene_symbol"],
        "query_ids": ["entrez_gene_id", "diseaseontology_id", "disease_name"],
        "annotate_syntax": "http://lynx.ci.uchicago.edu/gediresources/resources/genes/9606/*/diseases",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/lynx_disease_context.json")
        }
    },
    "reactome_lower": {
        "annotate_ids": ["reactome_id"],
        "query_ids": ["reactome_id", "pathway_name"],
        "annotate_syntax": "http://reactome.org/ContentService/data/pathways/low/diagram/entity/*/allForms?speciesId=48887",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/reactome_lower_context.json")
        }
    },
    "reactome": {
        "annotate_ids": ["reactome_id"],
        "query_ids": ["reactome_id"],
        "annotate_syntax": "http://localhost:8899/reactome/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/reactome_context.json")
        }
    },
    "static_protein_interaction": {
        "annotate_ids": ["uniprot_id"],
        "query_ids": ["uniprot_id"],
        "annotate_syntax": "http://reactome.org/ContentService/interactors/static/molecule/*/details?page=-1&pageSize=-1",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/protein_interaction_context.json")
        }
    },
    "openfda": {
        "annotate_ids": ["drug_symbol"],
        "query_ids": ["drug_effect", "pharmacology_class"],
        "annotate_syntax": "https://api.fda.gov/drug/event.json?search=generic_name:*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/openfda.json")
        }
    },
    "pharos": {
        "annotate_ids": ["uniprot_id", "hgnc_gene_symbol", "ensembl_gene_id"],
        "query_ids": ["disease_name", "omim_term", "chembl_id", "pdb_id", "mgi_term"],
        "annotate_syntax": "http://localhost:8899/pharos/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/pharos_context.json")
        }
    },
    "omicsdi": {
        "annotate_ids": ["pxd_id"],
        "query_ids": ["uniprot_id", "ensembl_protein_id"],
        "annotate_syntax": "http://localhost:8899/omicsdb/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/omicsdb_context.json")
        }
    },
    "biolinks_interaction": {
        "annotate_ids": ["entrez_gene_id"],
        "query_ids": ["entrez_gene_id", "mouse_gene_id"],
        "annotate_syntax": "http://localhost:8899/biolinks_interact/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__),"context/biolinks_interact_context.json")
        }
    },
    "civic_general": {
        "annotate_ids": ["hgnc_gene_symbol"],
        "query_ids": ["civic_gene_id", "civic_variant_id", "disease_name", "drug_symbol", "entrez_gene_id"],
        "annotate_syntax": "https://civic.genome.wustl.edu/api/variants/typeahead_results?limit=20&query=*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__), "context/civic_general_context.json")
        }
    },
    "civic_gene": {
        "annotate_ids": ["civic_gene_id"],
        "query_ids": ["civic_variant_id", "civic_variant_group_id", "civic_source_id", "hgnc_gene_symbol", "entrez_gene_id"],
        "annotate_syntax": "https://civic.genome.wustl.edu/api/genes/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__), "context/civic_gene_context.json")
        }
    },
    "civic_variant": {
        "annotate_ids": ["civic_variant_id"],
        "query_ids": ["hgnc_gene_symbol", "entrez_gene_id", "civic_gene_id", "so_id", "civic_evidience_id", "disease_name", "diseaseontology_id", "drug_symbol"],
        "annotate_syntax": "https://civic.genome.wustl.edu/api/variants/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__), "context/civic_variant_context.json")
        }
    },
    "civic_evidence": {
        "annotate_ids": ["civic_evidence_id"],
        "query_ids": ["hgnc_gene_symbol", "disease_name", "drug_symbol", "pubmed_id", "civic_variant_id"],
        "annotate_syntax": "https://civic.genome.wustl.edu/api/evidence_items/*",
        "jsonld": {
            "context_file_path": os.path.join(os.path.dirname(__file__), "context/civic_evidence_context.json")
        }
    }
}

CLIENT_LIST = {"mygene.info", "myvariant.info", "mydrug.info"}

def add_interaction_resources():
    url = 'http://reactome.org/ContentService/interactors/psicquic/resources'
    headers = {'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        doc = r.json()
        for _doc in doc:
            if _doc['active']:
                api_name = _doc['name'].lower() + '_interaction'
                annotate_syntax = 'http://reactome.org/ContentService/interactors/psicquic/molecule/' + _doc['name'] + '/*/details'
                AVAILABLE_API_SOURCES.update({api_name: {"annotate_ids": ['uniprot_id'], "query_ids": ["uniprot-id"],
                                                         "annotate_syntax": annotate_syntax, "jsonld": {"context_file_path":

                                                                                                        "context/protein_interaction_context.json"}}})

add_interaction_resources()
