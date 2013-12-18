import math
import json
import numpy as np

bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
print(bins)

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

def camelCase(word):
    return ' '.join(x[0].upper()+x[1:] for x in word.split('-'))

def getData(filename):
	with open(filename, 'r') as infile:
	    data=json.load(infile)
	return data

def getBinnedResults(dictionary):
	vec = []
	for sk in dictionary.keys():
		vec.append(dictionary[sk].values())
	hist,bin_edges = np.histogram(vec,bins=bins)
	print hist
	print map(lambda x: int(x*10000.0/sum(hist))/100.0, hist)
	return hist

#renameSkillList(skill_list)
def renameSkillList(skill_list):

        list_of_skills=[]
        for skill in skill_list:
                list_of_skills.append(skill)

        replacements = getData('manualreplacements.txt')

        for src, target in replacements.iteritems():
                list_of_skills.remove(src.replace('"',''))
                list_of_skills.append(target.replace('"',''))

        list_of_skills = map(lambda x: camelCase(x.strip()), list_of_skills)

        return list(set(list_of_skills))


print "----"
execfile("skill_list.py")
list1 = renameSkillList(skill_list)
list2 = getData('renamedcomplete.txt').keys()
print len(list1)
print len(list2)
print set(list2)-set(list1)
print set(list1)-set(list2)
list3 = list(set(list1+list2))
list3.sort()
print list3
print "----"

solargedata = getData('so-large/result.txt')
mathselargedata = getData('mathse-large/result.txt')
soquantlargedata = getData('so-quant-large/result.txt')
#soeleclargedata = getData('so-elec-large/result.txt')
wikilangdata = getData('wikilang/result.txt')
wiki_tfidfdata = getData('wiki_tfidf/result.txt')

print("so")
getBinnedResults(solargedata)
print("math-se")
getBinnedResults(mathselargedata)
print("so-quant")
getBinnedResults(soquantlargedata)
#getBinnedResults(soeleclargedata)
print("wiki-lang")
getBinnedResults(wikilangdata)
print("wiki_tfidf")
getBinnedResults(wiki_tfidfdata)
	
print "xxx"
	






