import math
import json
import numpy as np

bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
print(bins)

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

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
	
	






