from pyld import jsonld
import json
import re
import requests

t = jsonld.JsonLdProcessor()

'''
Input: jsonld document
Output: nquads format of the jsonld doc
'''
def jsonld2nquads(jsonld_doc):
	'''
	cmd = 'jsonld --validate --format nquads'
	p = Popen(cmd.split(), shell=True, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
	p.stdin.write(json.dumps(jsonld_doc).encode())
	stdout_data = p.communicate()[0]
	p.stdin.close()
	data_output = stdout_data.decode()
	print(data_output)
	'''
	# need to skip html escapes
	nquads = requests.post('http://jsonld.biothings.io/?action=nquads', data={'doc':json.dumps(jsonld_doc).replace('>', "&gt;").replace(' ','')})
	# remove the log line from the nquads
	nquads = re.sub('Parsed .*second.\n', '', nquads.json()['output'])
	return t.parse_nquads(nquads)

'''
given a predicate and object, return the value from nquads
'''
def fetchvalue(nquads, object_uri, predicate='http://www.w3.org/2004/02/skos/core#exactMatch'):
	results = []
	# check if it's a valid nquads
	if '@default' in nquads:
		for _nquad in nquads['@default']:
			if _nquad['predicate']['value'] == predicate and object_uri in _nquad['object']['value']:
				print(_nquad)
				results.append(_nquad['object']['value'].split(object_uri)[1])
	# if results is empty, it could be either nquads is empty or object_uri could not be found in nuqads
	if results:
		return list(set(results))
	else:
		return [None]