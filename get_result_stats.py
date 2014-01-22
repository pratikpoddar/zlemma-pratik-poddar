import math
import json
import numpy as np
from cluster import *
import networkx as nx
import operator

bins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

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

def getStatisticalChecks():
	def tf(vec):
		return 1
	
	mean_error_vecs = []
	d = getData('renamedcomplete.txt')
	keys = d.keys()
	for k in keys:
		v = filter(lambda x: 0.001 < x < 0.999, d[k].values())
		if v:
			if np.mean(v)>0.3:
				mean_error_vecs.append(k)
	return {'meanerror': mean_error_vecs}

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

def identify_non_reciprocative_pairs(filename, threshold_value):
	
	d = getData(filename)
	ks = d.keys()
		
	error_pairs = []
	for key1 in ks:
		for key2 in ks:
			if d[key1][key2]-d[key2][key1] > threshold_value:
				error_pairs.append((key1, key2))
	return error_pairs

def identify_non_transitive_triplets(filename):

	d = getData(filename)
	ks = d.keys()
	
	error_triplets = []
	for key1 in ks:
		for key2 in ks:
			if d[key1][key2] > 0.7:
				for key3 in ks:
					if d[key2][key3] > 0.7 and d[key1][key3]<0.7:
						error_triplets.append([key1, key2, key3])
	return error_triplets
	
def identify_clusters(filename, threshold):

	d = getData(filename)
	keys = d.keys()
	
	nparray = []
	for key1 in keys:
		nparray2 = []
		for key2 in keys:
			if max(d[key1][key2], d[key2][key1]) > threshold:
				nparray2.append(1)
			else:
				nparray2.append(0)
		nparray.append(nparray2)
	
	A = np.array(nparray)

	G = nx.from_numpy_matrix(A, create_using=nx.DiGraph())
	for subg in nx.strongly_connected_component_subgraphs(G):
	    print map(lambda x: keys[x], subg.nodes())

	return map(lambda subg: map(lambda x: keys[x], subg.nodes()), nx.strongly_connected_component_subgraphs(G))

def identify_big_numbers(filename, threshold):

	d = getData(filename)
	keys = d.keys()
	
	output = []
	print "Big Numbers on " + filename
	for key1 in keys:
		for key2 in keys:
			if (d[key1][key2] >= threshold) and (not (key1 == key2)):
				print key1 + ", " + key2 + " " + str(d[key1][key2]) + " (other side) " + str(d[key2][key1])
				output.append((key1, key2))
	return output

def identify_big_suspicious_numbers(filename, threshold):

        d = getData(filename)
        keys = d.keys()

        output = []
        print "Suspicious Big Numbers on " + filename
        for key1 in keys:
                for key2 in keys:
                        if (d[key1][key2] >= threshold) and (not (key1 == key2)):
				if d[key2][key1] < 0.01:
	                                print key1 + ", " + key2 + " " + str(d[key1][key2]) + " " + str(d[key2][key1])
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


def investigateSkill(filename, skill):

	d = getData(filename)
	n = transpose_dict_of_dicts(d)

	best_outgoing = dict(sorted(d[skill].iteritems(), key=operator.itemgetter(1), reverse=True)[:5]).keys()
	best_incoming = dict(sorted(n[skill].iteritems(), key=operator.itemgetter(1), reverse=True)[:5]).keys()
	nearest_neighbours = []
	for k in best_outgoing + best_incoming:
		nearest_neighbours.extend(dict(sorted(d[k].iteritems(), key=operator.itemgetter(1), reverse=True)[:3]).keys()+dict(sorted(n[k].iteritems(), key=operator.itemgetter(1), reverse=True)[:3]).keys())
		nearest_neighbours = list(set(nearest_neighbours))
	
	return {'best_outgoing': best_outgoing, 'best_incoming': best_incoming, 'nearest_neighbours': nearest_neighbours}

print "----"
execfile("skill_list.py")
list1 = renameSkillList(skill_list)
list2 = getData('renamedcomplete.txt').keys()
print "Number of Skills in Input File: " + str(len(list1))
print "Number of Skills in Output File: " + str(len(list2))
print "Skils in Output File not in Input File: " + str(set(list2)-set(list1))
print "Skils in Input File not in Output File: " + str(set(list1)-set(list2))
list3 = list(set(list1+list2))
list3.sort()
print "All Skills: " + str(list3)
#for s in list3:
#	print s
outfile = open('allskills.txt', 'w')
for s in list3:
	outfile.write(s)
	outfile.write('\n')
outfile.close()
list4 = getData('manualdepartmentmapping.txt').keys()
print "Skills in Department Mapping not in All Skills: " + str(set(list4)-set(list3))
print "Skills in All Skills not in Department Mapping: " + str(set(list3)-set(list4))
print "----"

k21 = getData('manualforcedinput.txt')
k22 = getData('manualinput.txt')
k3 = getData('manualreplacements.txt')
keys_in_manual_input = []
keys_in_manual_replacements = []
keys_in_manual_input += k21.keys() + k22.keys()
keys_in_manual_replacements += k3.keys()
for k in k21.keys():
	keys_in_manual_input += k21[k].keys()
for k in k22.keys():
        keys_in_manual_input += k22[k].keys()
print "Skills in Manual Input but not in Skill List: " + str(set(filter(lambda x: x not in skill_list, keys_in_manual_input)))
print "Skills in Manual Replacements but not in Skill List: " + str(filter(lambda x: x not in map(lambda x: camelCase(x), skill_list), keys_in_manual_replacements))
print "Skills that appear twice in Manual Replacements Values are: " + str(set([x for x in k3.values() if k3.values().count(x) > 1]))

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
print "Weak Nodes"
print weaknodes
print "----"

non_reciprocative_pairs = identify_non_reciprocative_pairs('manual_overridden_renamedresult.txt', 0.4)
print "Non Reciprocative Pairs on Manual_Overridden_Renamed_Result"
print non_reciprocative_pairs
print "----"

#non_reciprocative_pairs = identify_non_reciprocative_pairs('renamedcomplete.txt', 0.4)
#print "Non Reciprocative Pairs on Renamed_Complete"
#print non_reciprocative_pairs
print "----"

non_transitive_triplets = identify_non_transitive_triplets('manual_overridden_renamedresult.txt')
print "Non Transitive Triplets on Manual_Overridden_Renamed_Result"
print non_transitive_triplets
print "----"

print "----"
print "Big Numbers"
identify_big_numbers('renamedcomplete.txt', 0.8)
print "----"

print "----"
print "Big Suspicious Numbers"
identify_big_suspicious_numbers('renamedcomplete.txt', 0.8)
print "----"


print "----"
print "Clusters 1"
identify_possible_clusters('manual_overridden_renamedresult.txt', 0.8)
print "----"

print "----"
print "Clusters 2"
identify_possible_clusters('renamedcomplete.txt', 0.8)
print "----"

print "----"
print "Clusters 3"
identify_possible_clusters('renamedcomplete.txt', 0.9)
print "----"

print "----"
print "Cluster 4"
identify_clusters('renamedcomplete.txt', 0.7)
print "----"

print "----"
print "Cluster 5"
identify_clusters('renamedcomplete.txt', 0.6)
print "----"


print "----"
print "Statistical Checks: Mean Error"
print getStatisticalChecks()['meanerror']
print "----"

print "xxx"

print "----"
print "Investigating Algorithms Skill"	
print investigateSkill('renamedcomplete.txt', 'Algorithms')




