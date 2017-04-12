# biothings_explorer_web

### Project Website: 
    http://biothings.io/explorer_demo/
### Project Demo:
    https://goo.gl/sx34T2
    
### Project Description

RESTful APIs have been widely used to distribute biological data in a programmatic manner. And many popular biological APIs such as MyGene.info, MyVariant.info, Drugbank, Reactome, Wikipathways and Ensembl, all adopt JSON as their primary data format. These disparate API resources feature diverse types of biological entities, e.g. variants, genes, proteins, pathways, drugs, symptoms, and diseases. The integration of these API resources would greatly facilitate scientific domains such as translational medicine, where multiple types of biological entities are involved, and often from different resources. 

To fulfill the task of integrating API resources, We have designed a workflow using a semantic approach. In this workflow, a JSON-LD context file, which provides Universal Resource Identifier(URI) mapping for each API input/output types, is created for individual API resource, enhancing their interoperability. Besides, API metadata are collected and organized, e.g. query syntax, input/output types, allowing API calls to be generated automatically. By utilizing this workflow, we are able to link different API resources through the input/output types which they shared in common. For example, MyGene.info (http://mygene.info) adopts Entrez Gene ID as its input type, which is also one of the output types for MyVariant.info (http://myvariant.info). Thus, data in these two APIs could be linked together through Entrez Gene ID.

Following this workflow, we have developed a Python package as well as a web visualization interface named ‘BioThings Explorer’ using Cytoscape.js. These tools empower users to explore the relationship between different biological entities through the vast amount of biological data provided by various API resources in a visually organized manner. For example, users could easily explore all biological pathways in which a rare Mendelian disease candidate gene is involved, and then find all genes as well as chemical compounds which could regulate these biological pathways (Ipython Notebook Demo: https://goo.gl/sx34T2), thus providing potential treatment options.
