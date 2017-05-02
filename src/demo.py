from biothings import Graph
graph = Graph()
'''
Assume well-tolerated drugs: Fludarabine, Carmustine
Assume poorly-tolerated drugs: Etoposide, Tacrolimus
'''
drug_set1 = ['Fludarabine', 'Carmustine']
drug_set2 = ['Etoposide', 'Tacrolimus']

'''
Get DrugBank ID using drug and compound API (mydrug python package)
'''
import mydrug
md = mydrug.MyDrugInfo()
results_drug_set1 = md.querymany(drug_set1, scopes='drugbank.name', fields='drugbank.accession_number')
print(results_drug_set1)
set1d = [_record['drugbank']['accession_number'] for _record in results_drug_set1]
print('Drugbank ID list for Set1: {}'.format(set1d))


results_drug_set2 = md.querymany(drug_set2, scopes='drugbank.name', fields='drugbank.accession_number')
print(results_drug_set2)
set2d = [_record['drugbank']['accession_number'] for _record in results_drug_set2]
print('Drugbank ID list for Set2: {}'.format(set2d))

from biothings import IdListHandler
# IdListHandler is designed to handle a list of given IDs, e.g. drugbank ID, and return a list of IDs given the output type, e.g. uniprot_id
ih = IdListHandler()


'''
Use IdListHandler to retrieve a list of Uniprot_IDs correponding to Drugbank_IDs for Drug Set 1
'''
set1p = ih.list_handler(input_id_list=set1d, input_type='drugbank_id', output_type='uniprot_id')
print('Protein Uniprot IDs related to Drugs in Drug Set 1 is: {}'.format(set1p))
dict1p_d = ih.list_handler_for_graph(input_id_list=set1d, input_type='drugbank_id', output_type='uniprot_id')

'''
Use IdListHandler to retrieve a list of Uniprot_IDs correponding to Drugbank_IDs for Drug Set 2
'''
set2p = ih.list_handler(input_id_list=set2d, input_type='drugbank_id', output_type='uniprot_id')
print('Protein Uniprot IDs related to Drugs in Drug Set 2 is: {}'.format(set2p))
dict2p_d = ih.list_handler_for_graph(input_id_list=set2d, input_type='drugbank_id', output_type='uniprot_id')


'''
Use IdListHandler to retrieve a list of Entrez_Gene_IDs correponding to Uniprot_IDs for Drug Set 1
'''
set1g = ih.list_handler(input_id_list=set1p, input_type='uniprot_id', output_type='entrez_gene_id')
print('Entrez Gene IDs related to Drugs in Drug Set 1 is: {}'.format(set1g))
dict1g_p = ih.list_handler_for_graph(input_id_list=set1p, input_type='uniprot_id', output_type='entrez_gene_id')
'''
Use IdListHandler to retrieve a list of Entrez_Gene_IDs correponding to Uniprot_IDs for Drug Set 1
'''
set2g = ih.list_handler(input_id_list=set2p, input_type='uniprot_id', output_type='entrez_gene_id')
print('Entrez Gene IDs related to Drugs in Drug Set 1 is: {}'.format(set2g))
dict2g_p = ih.list_handler_for_graph(input_id_list=set2p, input_type='uniprot_id', output_type='entrez_gene_id')


'''
Use IdListHandler to retrieve a list of Wikipathway_IDs correponding to Entrez_Gene_IDs for Drug Set 1
'''
set1pw = ih.list_handler(input_id_list=set1g, input_type='entrez_gene_id', output_type='wikipathway_id')
print('Wikipathway IDs related to Drugs in Drug Set 1 is: {}'.format(set1pw))
dict1pw_g = ih.list_handler_for_graph(input_id_list=set1g, input_type='entrez_gene_id', output_type='wikipathway_id')
'''
Use IdListHandler to retrieve a list of Wikipathway_IDs correponding to Entrez_Gene_IDs for Drug Set 2
'''
set2pw = ih.list_handler(input_id_list=set2g, input_type='entrez_gene_id', output_type='wikipathway_id')
print('Wikipathway IDs related to Drugs in Drug Set 2 is: {}'.format(set2pw))
dict2pw_g = ih.list_handler_for_graph(input_id_list=set2g, input_type='entrez_gene_id', output_type='wikipathway_id')

'''
Use IdListHandler to retrieve a list of Entrez_Gene_IDs correponding to Wikipathway_IDs for Drug Set 1
'''
set1g_other = ih.list_handler(input_id_list=set1pw, input_type='wikipathway_id', output_type='entrez_gene_id')
dict1g_other_pw = ih.list_handler_for_graph(input_id_list=set1pw, input_type='wikipathway_id', output_type='entrez_gene_id')
'''
Use IdListHandler to retrieve a list of Entrez_Gene_IDs correponding to Wikipathway_IDs for Drug Set 2
'''
set2g_other = ih.list_handler(input_id_list=set2pw, input_type='wikipathway_id', output_type='entrez_gene_id')
dict2g_other_pw = ih.list_handler_for_graph(input_id_list=set2pw, input_type='wikipathway_id', output_type='entrez_gene_id')

graph.add_to_graph(dict1p_d)
graph.add_to_graph(dict2p_d)

graph.add_to_graph(dict1g_p)
graph.add_to_graph(dict2g_p)

graph.add_to_graph(dict1pw_g)
graph.add_to_graph(dict2pw_g)

