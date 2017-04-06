AVAILABLE_IDS= {"ensembl_gene_id": {
	"uri": "http://identifiers.org/ensembl.gene/",
	"example": "ENSG00000139618"
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
 	"uri": "http://identifiers.org/hgvs*/",
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
 }}

AVAILABLE_API_SOURCES={"mygene.info": {
 	"annotate_ids": ["entrez_gene_id", "ensembl_gene_id"],
 	"query_ids": ["uniprot_id", "ensembl_gene_id", "hgnc_gene_symbol", "wikipathway_id", "pubmed_id"],
 	"annotate_syntax": "http://mygene.info/v3/gene/*",
 	"query_syntax": "http://mygene.info/v3/query?q=*",
  "description": "gene annotation service",
 	"jsonld": {
 		"context_file_path": "context/mygene_context.json",
 		"data_source_uris": [
 			"http://schema.mygene.info/datasource/ensembl",
 			"http://schema.mygene.info/datasource/go",
 			"http://schema.mygene.info/datasource/homologene",
 			"http://schema.mygene.info/datasource/uniprot",
      "http://schema.mygene.info/datasource/generif",
      "http://schema.mygene.info/datasource/refseq",
      "http://schema.mygene.info/datasource/pathway",
      "http://schema.mygene.info/datasource/interpro"]
 	}
 },
  "myvariant.info": {
  	"annotate_ids": ["hgvs_id"],
  	"query_ids": ["entrez_gene_id", "hgnc_gene_symbol", "ensembl_gene_id", "dbsnp_id", "pubmed_id", "uniprot_id"],
  	"annotate_syntax": "http://myvariant.info/v1/variant/*",
  	"query_syntax": "http://myvariant.info/v1/query?q=*",
  	"jsonld": {
  		"context_file_path": "context/myvariant_context.json",
  		"data_source_uris": ["http://schema.myvariant.info/datasource/cadd",
            "http://schema.myvariant.info/datasource/clinvar",
            "http://schema.myvariant.info/datasource/dbnsfp",
            "http://schema.myvariant.info/datasource/dbsnp",
            "http://schema.myvariant.info/datasource/docm",
            "http://schema.myvariant.info/datasource/emv",
            "http://schema.myvariant.info/datasource/evs",
            "http://schema.myvariant.info/datasource/gwassnps",
            "http://schema.myvariant.info/datasource/mutdb",
            "http://schema.myvariant.info/datasource/snpeff",
            "http://schema.myvariant.info/datasource/grasp"]
  	}
  },
  "mydrug.info": {
  	"annotate_ids": ["drugbank_id"],
  	"query_ids": ["dbsnp_id", "pubchem_id", "drugbank_id", "pubmed_id", "hgnc_gene_symbol", "uniprot_id", "clinicaltrial_id"],
  	"annotate_syntax": "http://c.biothings.io/v1/drug/*",
  	"query_syntax": "http://c.biothings.io/v1/query?q=*",
  	"jsonld": {
  		"context_file_path": "context/mydrug_context.json",
  		"data_source_uris": [
  		    "http://schema.mydrug.info/datasource/drugbank",
  			  "http://schema.mydrug.info/datasource/pharmgkb"
  			]
  	}
  },
  "clinicaltrials.gov": {
  	"annotate_ids": ["clinicaltrial_id"],
  	"annotate_syntax": "http://clinicaltrialsapi.cancer.gov/v1/clinical-trial/*"
  },
  "wikipathways": {
  	"annotate_ids": ["wikipathway_id"],
  	"annotate_syntax": "http://http://webservice.wikipathways.org/getPathwayInfo?pwId=*&format=json"
  },
  "uniprot": {
  	"annotate_ids": ["uniprot_id"],
  	"annotate_syntax": "http://www.ebi.ac.uk/proteins/api/variation/*",
  	"jsonld": {
  		"context_file_path": "context/uniprot_context.json",
  		"data_source_uris": [
  			"http://schema.uniprot.info/datasource/features"]
  	}
  },
  "lynx_pathway": {
    "annotate_ids": ["hgnc_gene_symbol"],
    "annotate_syntax": "http://lynx.ci.uchicago.edu/gediresources/resources/genes/9606/*/pathways"
  },
  "lynx_diseases": {
    "annotate_ids": ["hgnc_gene_symbol"],
    "annotate_syntax": "http://lynx.ci.uchicago.edu/gediresources/resources/genes/9606/*/diseases"
  },
  "lynx_interactions": {
    "annotate_ids": ["hgnc_gene_symbol"],
    "annotate_syntax": "http://lynx.ci.uchicago.edu/gediresources/resources/genes/9606/*/interactions"
  },
  "lynx_symptoms": {
    "annotate_ids": ["hgnc_gene_symbol"],
    "annotate_syntax": "http://lynx.ci.uchicago.edu/gediresources/resources/genes/9606/*/symptoms"
  },
  "lynx_brainconnectivity": {
    "annotate_ids": ["hgnc_gene_symbol"],
    "annotate_syntax": "http://lynx.ci.uchicago.edu/gediresources/resources/genes/9606/*/brainconnectivity"
  },
  "genenames.org": {
    "annotate_ids": ["hgnc_gene_symbol"],
    "annotate_syntax": "http://rest.genenames.org/fetch/symbol/*"
  },
  "expression_array": {
    "annotate_ids": ["pubmed_id"],
    "annotate_syntax": "https://www.ebi.ac.uk/arrayexpress/json/v3/experiments?pmid=*"
  }}

CONTEXT_FILE_PATHS={"mygene.info": "context/mygene_context.json",
   "myvariant.info": "context/myvariant_context.json",
   "mydrug.info": "context/mydrug_context.json"
  }

CLIENT_LIST = {"mygene.info", "myvariant.info", "mydrug.info"}

