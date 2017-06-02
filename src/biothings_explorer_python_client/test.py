'''
Assume well-tolerated drugs: Fludarabine, Carmustine
'''
drug_set1 = ['Fludarabine', 'Carmustine']

'''
Import biothings_explorer python package
'''
from biothings_explorer import IdListHandler
ih = IdListHandler()

'''
Get DrugBank ID
'''
set1d = ih.list_handler(input_id_list=drug_set1, input_type='drug_symbol', output_type='drugbank_id')

'''
Use IdListHandler to retrieve a list of Uniprot_IDs correponding to Drugbank_IDs for Drug Set 1
'''
set1p = ih.list_handler(input_id_list=set1d, input_type='drugbank_id', output_type='uniprot_id', relation="oban:is_Target_of")
print('Protein Uniprot IDs related to Drugs in Drug Set 1 is: {}'.format(set1p))

'''
Use IdListHandler to retrieve a list of Entrez_Gene_IDs correponding to Uniprot_IDs for Drug Set 1
'''
set1g = ih.list_handler(input_id_list=set1p, input_type='uniprot_id', output_type='entrez_gene_id')
print('Entrez Gene IDs related to Drugs in Drug Set 1 is: {}'.format(set1g))

'''
Use IdListHandler to retrieve a list of Wikipathway_IDs correponding to Entrez_Gene_IDs for Drug Set 1
'''
set1pw = ih.list_handler(input_id_list=set1g, input_type='entrez_gene_id', output_type='wikipathway_id')
print('Wikipathway IDs related to Drugs in Drug Set 1 is: {}'.format(set1pw))