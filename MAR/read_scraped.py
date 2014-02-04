import json

output = {}

def process_keywords_data(filename):

	with open(filename, 'r') as f:
	    read_data = f.read()
	j = json.loads(read_data)

	kd_data_list = j['Keywords_data']

	for kd_data in kd_data_list:
		v1 = kd_data['CDATA'].find('=')+3
		v2 = kd_data['CDATA'][v1:].find(']')
		kds = kd_data['CDATA'][v1:][:v2]
		kds = map(lambda x: x.replace('"','').strip(), kds.split(','))
		kds = map(lambda x: x.split('__')[0], kds)
		output[kd_data['Keyword']] = kds

process_keywords_data('CS_10to15k')
