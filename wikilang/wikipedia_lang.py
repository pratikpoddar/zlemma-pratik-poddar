import json
import itertools
import sys

json_data=open('wikipedia_lang_2.json')
json_data_application=open('wikipedia_lang_3.json')
data = json.load(json_data)
data_application=json.load(json_data_application)

def printMatrix(skills, outputdict):
        skillset = []
        for skillx in skills:
                for skilly in skills:
                        try:                    
                                if outputdict[skillx][skilly] > 0.02:
                                        skillset.append(skillx)
                                        skillset.append(skilly)
                        except:
                                pass
        skills = list(set(skillset))

        row = '\t'
        for skillx in skills:
                row += skillx + '\t'
        print row

        for skilly in skills:
                row = skilly + '\t'
                for skillx in skills:
                        try:
                                if outputdict[skillx][skilly] < 0.02:
                                        row += str("")+'\t'
                                else:
                                        row += str("{0:.2f}".format(outputdict[skillx][skilly]))+'\t'
                        except Exception as e:
                                row += str("")+'\t'
                print row

	return

def getRelationship(skill1, skill2):
	try:
		vec1 = data[skill1].split(',')
		vec2 = data[skill2].split(',')
		vec1app = data_application[skill1]
		vec2app = data_application[skill2]
		print vec1
		print vec2
		print vec1app
		print vec2app
		common = list(set(vec1) & set(vec2))
		commonapplication = list(set(vec1app) & set(vec2app))
		totalapplications = list(set(vec1app + vec2app))
		value = 0.0
		for eachcommon in common:
			try:
				value+= 0.5/(2**(vec1.index(eachcommon)+vec2.index(eachcommon)))
			except:
				pass
		if len(commonapplication) and len(totalapplications):
			value=value*len(commonapplication)/(len(totalapplications)**(0.5))
		
		print skill1 + " " + skill2 + " " + str(value)

		return value
	except:
		return None

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

if not len(sys.argv) == 2:
	print "Usage : python wikipedia_lang.py saveresults"
	sys.exit(1)

if sys.argv[1] not in ["saveresults"]:
	print "Usage : python wikipedia_lang.py saveresults"
	sys.exit(1)

execfile("../skill_list.py")
skills = skill_list
skills2 = map(lambda x: slugify(x), skills)
print skills2

if sys.argv[1] == "saveresults":
	outputdict = {}
	for skill in skills2:
		outputdict[skill] = {}

	for comb in itertools.permutations(skills2,2):
        	val = getRelationship(comb[0], comb[1])
		if val:
		        outputdict[comb[0]][comb[1]] = val
		else:
			outputdict[comb[0]][comb[1]] = 0.0

	print outputdict
	printMatrix(skills2, outputdict)
	with open('result.txt', 'w') as infile:
		infile.write(json.dumps(outputdict))

	execfile("../floyd-warshall.py")
	completematrix=floydwarshall(outputdict, skills)
	with open('complete.txt', 'w') as infile:
		infile.write(json.dumps(completematrix))


