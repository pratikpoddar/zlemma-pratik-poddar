import math
import json
import numpy as np
from cluster import *

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
                list_of_skills.append(camelCase(skill))

        merge_replacements = {'Algorithms': 'Algorithm Theory', 'Statistics': 'Algorithm Theory'}
	merge_replacements = getData('manualreplacements.txt')

        removekeys = merge_replacements.keys()
        addkeys = []
        for k in merge_replacements.values():
                addkeys.append(k)

        removekeys = list(set(removekeys))
        addkeys = list(set(addkeys))

        print removekeys
        print addkeys
        for k in removekeys:
		try:
	                list_of_skills.remove(k)
		except Exception as e:
			print str(e)
			pass
        for k in addkeys:
                list_of_skills.append(k)

        return list(set(list_of_skills))


def transpose_dict_of_dicts(d):
  n = {}
  for i in d:
    for j in d[i]:
      if not (j in n):
        n[j] = {}
      n[j][i] = d[i][j]

  return n

def identifyWeakNodes(filename, threshold_func):
	d = getData(filename)
 	keys = d.keys()
	outbound_pain = []
	for key in keys:
		if not threshold_func(d[key].values()):
			outbound_pain.append(key)

	n = transpose_dict_of_dicts(d)
	keys = n.keys()
	inbound_pain = []
	for key in keys:
		if not threshold_func(n[key].values()):
			inbound_pain.append(key)

	return {'o': outbound_pain, 'i': inbound_pain }

def identify_clusters(filename):

	d = getData(filename)
	keys = d.keys()
	
	print "Hierarchical Clustering on " + filename
	cl = HierarchicalClustering(keys, lambda x,y: 0-math.log(max(d[x][y],d[y][x],0.0001)))
	for c in cl.getlevel(1):
		print c

	return cl.getlevel(1)

	#nparray = []
	#for key1 in keys:
	#	nparray2 = []
	#	for key2 in keys:
	#		nparray2.append(max(d[key1][key2], d[key2][key1]))
	#	nparray.append(nparray2)
	
	#A = np.array(nparray)

	#G = nx.from_numpy_matrix(A, create_using=nx.DiGraph())
	#for subg in nx.strongly_connected_component_subgraphs(G):
	#    print map(lambda x: keys[x], subg.nodes())

	#return map(lambda subg: map(lambda x: keys[x], subg.nodes()), nx.strongly_connected_component_subgraphs(G))

def identify_big_numbers(filename, threshold):

	d = getData(filename)
	keys = d.keys()
	
	output = []
	print "Big Numbers on " + filename
	for key1 in keys:
		for key2 in keys:
			if (d[key1][key2] >= threshold) and (not (key1 == key2)):
				print key1 + " " + key2 + " " + str(d[key1][key2])
				output.append((key1, key2))
	return output

def identify_possible_clusters(filename, threshold):

        d = getData(filename)
        keys = d.keys()

        print "Possible Clusters on " + filename
	list_of_clusters = []
	for key in keys:
		list_of_clusters.append([key])

	try:
	        for key1 in keys:
	                for key2 in keys:
        	                if (d[key1][key2] > threshold) and (not (key1 == key2)):
					cluster1 = filter(lambda x: key1 in x, list_of_clusters)[0]
					cluster2 = filter(lambda x: key2 in x, list_of_clusters)[0]

					if cluster1 != cluster2:
						list_of_clusters.remove(cluster1)
						list_of_clusters.remove(cluster2)
						list_of_clusters.append(cluster1+cluster2)
						
	except Exception as e:
		print e
		pass
	
	for cluster in list_of_clusters:
		if (len(cluster))>1:
			print cluster

        return list_of_clusters


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
for s in list3:
	print s
outfile = open('allskills.txt', 'w')
for s in list3:
	outfile.write(s)
	outfile.write('\n')
outfile.close()
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
print "----"

print "----"
s1 = getData('manual_overridden_renamedresult.txt').keys()
with open('allskills.txt') as f:
        s2 = map(lambda x : x.replace('\n',''), f.readlines())
print set(s1)-set(s2)
print set(s2)-set(s1)
print len(s1)
print len(s2)
print "----"

print "----"
def tf(l):
	high_values = len(filter(lambda x: x>=0.7, l))
	if high_values < 1:
		return False
	if high_values > len(l)/3:
		return False

	return True

weaknodes = identifyWeakNodes('renamedcomplete.txt', tf)
print weaknodes
print "----"
	
print "----"
identify_big_numbers('renamedcomplete.txt', 0.7)
print "----"

print "----"
identify_possible_clusters('renamedcomplete.txt', 0.6)
print "----"

print "----"
identify_possible_clusters('renamedcomplete.txt', 0.8)
print "----"

print "----"
identify_possible_clusters('renamedcomplete.txt', 0.9)
print "----"


print "xxx"
	






