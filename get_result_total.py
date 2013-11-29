import urllib2
import math
import itertools
import functools32
import sys
import json

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

def getData(filename):
	with open(filename, 'r') as infile:
	    data=json.load(infile)
	return data

if sys.argv[1] == "downloaddata":
	sys.exit(1)	

if sys.argv[1] == "saveresults":
	sys.exit(1)

if sys.argv[1] == "mergeresults":
	solargedata = getData('so-large/result.txt')
	mathselargedata = getData('mathse-large/result.txt')
	wikilangdata = getData('wikilang/result.txt')
	wiki_tfidfdata = getData('wiki_tfidf/result.txt')
	
	def getMerged(skill1, skill2):
	
		if skill1 == skill2:
			return 1.0

		try:
			return solargedata[skill1][skill2]
		except:
			pass

		try:
			return mathselargedata[skill1][skill2]
		except:
			pass

		try:
			return wikilangdata[skill1][skill2]
		except:
			pass
	
		try:
			return wiki_tfidfdata[skill1][skill2]
		except:
			pass
	
		return 0.0

	skill_total = list(set(solargedata.keys() + mathselargedata.keys() + wikilangdata.keys() + wiki_tfidfdata.keys()))
	
	outputdict = {}
        for skill in skill_total:
                outputdict[skill] = {}

	for comb in itertools.permutations(skill_total,2):
                outputdict[comb[0]][comb[1]] = getMerged(comb[0], comb[1])

        print outputdict
        with open('result.txt', 'w') as infile:
                infile.write(json.dumps(outputdict))

        execfile("floyd-warshall.py")
        completematrix=floydwarshall(outputdict, skill_total)
        with open('complete.txt', 'w') as infile:
                infile.write(json.dumps(completematrix))
	

