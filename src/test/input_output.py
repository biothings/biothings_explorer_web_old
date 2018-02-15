input_output_dict = {
	"http://mygene.info/v3/gene/{geneid}": [
    {
		"input": {
			"http://identifiers.org/ncbigene/": "1017"
		},
		"output": {
			"http://identifiers.org/hgnc.symbol/": "CDK2",
			"http://identifiers.org/unigene/": "Hs.689624",
            "http://identifiers.org/uniprot/": "P24941",
            "http://identifiers.org/pdb/": "1AQ1",
            "http://identifiers.org/biocarta.pathway/": "fbw7pathway",
            "http://identifiers.org/kegg.pathway/": "hsa04068",
            "http://identifiers.org/reactome/": "R-HSA-109582",
            "http://identifiers.org/pubmed/": "11907280",
            "http://identifiers.org/go/": "0000082"
		}
	}],
    "http://mygene.info/v3/query": [
    {
        "input": {
            "http://identifiers.org/hgnc.symbol/": "CDK7"
        },
        "output": {
            "http://identifiers.org/ncbigene/": "1022",
            "http://identifiers.org/taxonomy/": "9606"
        }
    },
    {
        "input": {
            "http://identifiers.org/wikipathways/": "WP1530"
        },
        "output": {
            "http://identifiers.org/ncbigene/": "166979",
            "http://identifiers.org/taxonomy/": "9606"
        }
    },
    {
        "input": {
            "http://identifiers.org/uniprot/": "P24941"
        },
        "output": {
            "http://identifiers.org/ncbigene/": "1017",
            "http://identifiers.org/taxonomy/": "9606"
        }
    }],
    "http://mychem.info/v1/query": [
    {
        "input": {
            "http://identifiers.org/rxcui/": "35623"
        },
        "output": {
            "http://identifiers.org/inchikey/": "FTALBRSUTCGOEG-UHFFFAOYSA-N",
            "http://identifiers.org/unii/": "7LJ087RS6F",
            "http://biothings.io/terms/drugname/": "Riluzole",
            "http://identifiers.org/pubchem.compound/": "5070",
            "http://identifiers.org/iuphar.ligand/": "2326",
            "http://identifiers.org/chebi/": "8863",
            "http://identifiers.org/drugbank/": "DB00740"
        }
    }],
    "http://mychem.info/v1/drug/{drugid}": [
    {
        "input": {
            "http://identifiers.org/inchikey/": "PGBHMTALBVVCIT-VCIWKGPPSA-N"
        },
        "output": {
            "http://biothings.io/terms/drugname/": "Framycetin",
            "http://identifiers.org/unii/": "4BOC774388",
            "http://identifiers.org/uniprot/": "P0A7S3",
            "http://identifiers.org/drugbank/": "DB00452",
            "http://identifiers.org/pubmed/": "25129497",
            "http://identifiers.org/rxcui/": "4556",
            "http://identifiers.org/chebi/": "7508",
            "http://identifiers.org/chembl.compound/": "CHEMBL184618",
            "http://identifiers.org/kegg.drug/": "D05140",
            "http://identifiers.org/kegg.compound/": "C01737",
            "http://identifiers.org/iuphar.ligand/": "709",
            "http://identifiers.org/pharmgkb.drug/": "PA164743181",
            "http://identifiers.org/pubchem.compound/": "8378",
            "http://identifiers.org/pubchem.substance/": "46508892"
        }
    }],
    "http://myvariant.info/v1/variant/{variantid}": [
    {
        "input": {
            "http://identifiers.org/hgvs/": "chr6:g.26093141G>A"
        },
        "output": {
            "http://identifiers.org/dbsnp/": "rs1800562",
            "http://identifiers.org/hgnc.symbol/": "HFE",
            "http://identifiers.org/ensembl.gene/": "ENSG00000010704",
            "http://identifiers.org/ensembl.transcript/": "ENST00000357618",
            "http://identifiers.org/ccds/": "CCDS4578.1",
            "http://identifiers.org/uniprot/": "Q6B0J5",
            "http://identifiers.org/clinvar.record/": "RCV000308358",
            "http://identifiers.org/clinvar/": "9",
            "http://identifiers.org/omim.disease/": "612635",
            "http://identifiers.org/omim.variant/": "613609.0001",
            "http://identifiers.org/ncbigene/": "3077",
            "http://identifiers.org/ensembl.protein/": "ENSP00000380217",
            "http://identifiers.org/pubmed/": "24097068",
            "http://identifiers.org/clinicalsignificance/": "Pathogenic"
        }
    }],
	"https://www.ebi.ac.uk/chembl/api/data/target": [
    {
		"input": {
			"http://identifiers.org/uniprot/": "P30277"
		},
		"output": {
			"http://identifiers.org/chembl.target/": "CHEMBL2093"
		}
	}],
    "https://www.ebi.ac.uk/chembl/api/data/mechanism": [
    {
        "input": {
            "http://identifiers.org/chembl.target/": "CHEMBL2326"
        },
        "output": {
            "http://identifiers.org/chembl.compound/": "CHEMBL19"
        }
    }],
    "https://www.ebi.ac.uk/chembl/api/data/drug_indication": [
    {
        "input": {
            "http://identifiers.org/chembl.compound/": "CHEMBL19"
        },
        "output": {
            "http://identifiers.org/mesh.disease/": "D005901",
            "http://identifiers.org/efo/": "0000516"
        }
    }],
    "http://rest.ensembl.org/taxonomy/id/{taxonomyid}": [
    {
        "input": {
            "http://identifiers.org/taxonomy/": "9606"
        },
        "output": {
            "http://identifiers.org/taxonomy/": "9605"
        }
    }],
    "http://rest.ensembl.org/lookup/id/{geneid}": [
    {
        "input": {
            "http://identifiers.org/ensembl.gene/": "ENSG00000157764"
        },
        "output": {
            "http://identifiers.org/ensembl.exon/": "ENSE00003685923",
            "http://identifiers.org/ensembl.protein/": "ENSP00000288602",
            "http://identifiers.org/efo/": "0000365",
            "http://identifiers.org/hp/": "0004808"
        }
    }],
    "https://rest.genenames.org/fetch/{gene}": [
    {
        "input": {
            "http://identifiers.org/hgnc.symbol/": "CDK7"
        },
        "output": {
            "http://identifiers.org/hgnc/": "1778",
            "http://identifiers.org/ncbigene/": "1022",
            "http://identifiers.org/mgi/": "102956",
            "http://identifiers.org/refseq/": "NM_001799",
            "http://identifiers.org/ccds/": "CCDS3999",
            "http://identifiers.org/ensembl.gene/": "ENSG00000134058",
            "http://identifiers.org/omim.gene/": "601955",
            "http://identifiers.org/uniprot/": "P50613",
            "http://identifiers.org/rgd/": "621124"
        }
    },
    {
       "input": {
            "http://identifiers.org/hgnc/": "1022"
        },
        "output": {
            "http://identifiers.org/hgnc.symbol/": "BCYRN1",
            "http://identifiers.org/ncbigene/": "618",
            "http://identifiers.org/refseq/": "NR_001568",
            "http://identifiers.org/ensembl.gene/": "ENSG00000236824",
            "http://identifiers.org/omim.gene/": "606089"        } 
    }],
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi/{pubmedid}": [
    {
        "input": {
            "http://identifiers.org/pubmed/": "9858834"
        },
        "output": {
            "http://identifiers.org/pubmed/": "2143747"
        }
    }],
    "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={publicationid}": [
    {
        "input": {
            "http://identifiers.org/pubmed/": "20466091"
        },
        "output": {
            "http://identifiers.org/pmc/": "PMC2869000",
            "http://identifiers.org/doi/": "10.1016/j.ajhg.2010.04.006"
        }
    }],
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/genesymbol/{genesymbol}/aids/JSON": [
    {
        "input": {
            "http://identifiers.org/hgnc.symbol/": "CDK7"
        },
        "output": {
            "http://identifiers.org/pubchem.bioassay/": "1380"
        }
    }],
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/geneid/{geneid}/aids/JSON": [
    {
        "input": {
            "http://identifiers.org/ncbigene/": "1017"
        },
        "output": {
            "http://identifiers.org/pubchem.bioassay/": "1433"
        }
    }],
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{bioassayid}/sids/JSON": [
    {
        "input": {
            "http://identifiers.org/pubchem.bioassay/": "650"
        },
        "output": {
            "http://identifiers.org/pubchem.substance/": "856108"
        }
    }],
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/{bioassayid}/cids/JSON": [
    {
        "input": {
            "http://identifiers.org/pubchem.bioassay/": "650"
        },
        "output": {
            "http://identifiers.org/pubchem.compound/": "2142225"
        }
    }],
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{compoundid}/sids/JSON": [
    {
        "input": {
            "http://identifiers.org/pubchem.compound/": "2244"
        },
        "output": {
            "http://identifiers.org/pubchem.substance/": "4594"
        }
    }],
    "https://pubchem.ncbi.nlm.nih.gov/rest/pug/substance/sid/{substanceid}/cids/JSON": [
    {
        "input": {
            "http://identifiers.org/pubchem.substance/": "4594"
        },
        "output": {
            "http://identifiers.org/pubchem.compound/": "2244"
        }
    }],
    "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{goid}/ancestors": [
    {
        "input": {
            "http://identifiers.org/go/": "GO:0000082"
        },
        "output": {
            "http://identifiers.org/go/": "0008150"
        }
    }],
    "https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/{goid}/descendants": [
    {
        "input": {
            "http://identifiers.org/go/": "GO:0000082"
        },
        "output": {
            "http://identifiers.org/go/": "0071931"
        }
    }],
    "http://dgidb.genome.wustl.edu/api/v2/interactions.json?drugs={drugname}": [
    {
        "input": {
            "http://biothings.io/terms/drugname/": "riluzole"
        },
        "output": {
            "http://identifiers.org/hgnc.symbol/": "SCN5A",
            "http://identifiers.org/ncbigene/": "6331"
        }
    },
    {
        "input": {
            "http://identifiers.org/chembl.compound/": "CHEMBL1743018"
        },
        "output": {
            "http://identifiers.org/hgnc.symbol/": "HGF",
            "http://identifiers.org/ncbigene/": "3082"
        }
    }],
    "http://dgidb.genome.wustl.edu/api/v2/interactions.json?genes={genesymbol}": [
    {
        "input": {
            "http://identifiers.org/hgnc.symbol/": "HGF"
        },
        "output": {
            "http://biothings.io/terms/drugname/": "FORETINIB",
            "http://identifiers.org/chembl.compound/": "CHEMBL1230609"
        }
    }],
    "http://www.disease-ontology.org/api/metadata/{doid}": [
    {
        "input": {
            "http://identifiers.org/doid/": "DOID:678"
        },
        "output": {
            "http://identifiers.org/mesh.disease/": "D013494",
            "http://identifiers.org/snomedct/": "192975003",
            "http://identifiers.org/ncit/": "C85028",
            "http://identifiers.org/omim.disease/": "601104",
            "http://identifiers.org/umls/": "C0038868"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/disease/{diseaseid}/genes": [
    {
        "input": {
            "http://identifiers.org/omim.disease/": "601104"
        },
        "output": {
            "http://identifiers.org/hgnc/": "6893"
        }
    },
    {
        "input": {
            "http://identifiers.org/doid/": "DOID:678"
        },
        "output": {
            "http://identifiers.org/hgnc/": "10956",
            "http://identifiers.org/ncbigene/": "105374846"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/disease/{diseaseid}/phenotypes": [
    {
        "input": {
            "http://identifiers.org/omim.disease/": "601104"
        },
        "output": {
            "http://identifiers.org/hp/": "0000605"
        }
    },
    {
        "input": {
            "http://identifiers.org/doid/": "DOID:678"
        },
        "output": {
            "http://identifiers.org/hp/": "0000514"
        }
    },
    {
        "input": {
            "http://identifiers.org/orphanet/": "1934"
        },
        "output": {
            "http://identifiers.org/hp/": "0002133"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/gene/{geneid}/homologs": [
    {
        "input": {
            "http://identifiers.org/ncbigene/": "4750"
        },
        "output": {
            "http://identifiers.org/ncbigene/": "100520589",
            "http://identifiers.org/mgi/": "97303"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/gene/{geneid}/interactions": [
    {
        "input": {
            "http://identifiers.org/ncbigene/": "4750"
        },
        "output": {
            "http://identifiers.org/hgnc/": "3659"
        }
    },
    {
        "input": {
            "http://identifiers.org/hgnc/": "3659"
        },
        "output": {
            "http://identifiers.org/hgnc/": "19048"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/gene/{geneid}/phenotypes": [
    {
        "input": {
            "http://identifiers.org/ncbigene/": "4750"
        },
        "output": {
            "http://identifiers.org/hp/": "0000110"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/gene/{geneid}/pathways": [
    {
        "input": {
            "http://identifiers.org/ncbigene/": "1017"
        },
        "output": {
            "http://identifiers.org/reactome/": "R-HSA-69304"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/variant/{variantid}/genes": [
    {
        "input": {
            "http://identifiers.org/clinvar/": "9"
        },
        "output": {
            "http://identifiers.org/reactome/": "4886"
        }
    }],
    "https://api.monarchinitiative.org/api/bioentity/variant/{variantid}/genes": [
    {
        "input": {
            "http://identifiers.org/clinvar/": "9"
        },
        "output": {
            "http://identifiers.org/reactome/": "4886"
        }
    }],
    "http://c.biothings.io/v1/taxonomy/{taxonomyid}": [
    {
        "input": {
            "http://identifiers.org/taxonomy/": "9606"
        },
        "output": {
            "http://identifiers.org/taxonomy/": "9605"
        }
    }]
}