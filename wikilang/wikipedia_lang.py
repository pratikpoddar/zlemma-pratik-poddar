import json
import itertools
json_data=open('wikipedia_lang_2.json')
data = json.load(json_data)

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
	vec1 = data[skill1].split(',')
	vec2 = data[skill2].split(',')
	common = list(set(vec1) & set(vec2))
	value = 0.0
	for eachcommon in common:
		try:
			value+= 0.5/(2**(vec1.index(eachcommon)+vec2.index(eachcommon)))
		except:
			pass
		
	print skill1 + " " + skill2 + " " + str(value)

	return value

skills2 = ["c++", "java", "python", "ruby", "scala", "lisp"]

outputdict = {}
for skill in skills2:
	outputdict[skill] = {}

for comb in itertools.permutations(skills2,2):
	val = getRelationship(comb[0], comb[1])
	outputdict[comb[0]][comb[1]] = val

printMatrix(skills2, outputdict)



