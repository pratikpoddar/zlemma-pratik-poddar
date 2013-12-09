import json

def getData(filename):
        with open(filename, 'r') as infile:
            data=json.load(infile)
        return data

dictionary = getData('manual_overridden_renamedresult.txt')
dictionary2 = {}

for key1 in dictionary.keys():
	for key2 in dictionary[key1].keys():
		if dictionary[key1][key2] > 0.8:
			try:
				dictionary2[key1][key2] = dictionary[key1][key2]
			except:
				dictionary2[key1] = {}
				dictionary2[key1][key2] = dictionary[key1][key2]
			
with open('critical_results.txt', 'w') as infile:
    infile.write(json.dumps(dictionary2))

