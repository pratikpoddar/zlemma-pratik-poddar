import urllib2
import math
import itertools
import functools32
import sys
import json
import subprocess

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

def getData(filename):
	with open(filename, 'r') as infile:
	    data=json.load(infile)
	return data

def getDiff(pathnew, pathold, pathdiff):

	dictnew = getData(pathnew)
	dictold = getData(pathold)
	
	knew = dictnew.keys()
	kold = dictold.keys()
	addedkeys = filter(lambda x: x not in kold, knew)
	deletedkeys = filter(lambda x: x not in knew, kold)
	commonkeys = list(set(knew) and set(kold))

	bigchanges = []

	for comb in itertools.permutations(commonkeys,2):
		try:
			if abs(dictnew[comb[0]][comb[1]] - dictold[comb[0]][comb[1]]) > 0.15:
				bigchanges.append({'skill1':comb[0], 'skill2':comb[1], 'oldval':dictold[comb[0]][comb[1]], 'newval':dictnew[comb[0]][comb[1]]})
		except Exception as e:
			print "getDiff Error: " + str(e)

	diffoutput = {'deletedkeys': deletedkeys, 'addedkeys': addedkeys, 'bigchanges': bigchanges}
	
	with open(pathdiff, 'w') as infile:
		infile.write(json.dumps(diffoutput))

	return


def getRenamed(pathold, pathrenamed):
	
	infile = open(pathold)
	outfile = open(pathrenamed, 'w')

	replacements = getData('manualreplacements.txt')

	for line in infile:
	    for src, target in replacements.iteritems():
	        line = line.replace(src, target)
	    outfile.write(line)
	infile.close()
	outfile.close()

	return

def modifyManualInput(dictionary):
	
        manualoverride = getData('manualinput.txt')
        for key1 in manualoverride.keys():
		for key2 in manualoverride[key1].keys():
			try:
				dictionary[key1][key2] = float(manualoverride[key1][key2])
			except Exception as e:
				print "Exception while modifying outputdict with manual override " + key1 + " " + key2

        return dictionary

def modifyManualInputForced(dictionary):
	
	manualoverride = getData('manualforcedinput.txt')
	new_keys = []
        for key1 in manualoverride.keys():
                for key2 in manualoverride[key1].keys():
			new_keys.append(key1)
			new_keys.append(key2)

	new_keys = list(set(new_keys))

	for key in new_keys:
		if key not in dictionary.keys():
			dictionary[key]={}

	for key in new_keys:
		for keyold in dictionary.keys():
			try:
				dictionary[keyold][key] = float(manualoverride[keyold][key])
			except:
				try:
					dictionary[keyold][key] = dictionary[keyold][key]
				except:
					dictionary[keyold][key] = 0.0
		
        return {'skills': dictionary.keys(), 'outputdict': dictionary}
	

if sys.argv[1] == "downloaddata":
	sys.exit(1)	

if sys.argv[1] == "saveresults":
	sys.exit(1)

if sys.argv[1] == "mergeresults":
	solargedata = getData('so-large/result.txt')
	mathselargedata = getData('mathse-large/result.txt')
	soquantlargedata = getData('so-quant-large/result.txt')
	#soeleclargedata = getData('so-elec-large/result.txt')
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
                        return soquantlargedata[skill1][skill2]
                except:
                        pass

                #try:
                #        return soeleclargedata[skill1][skill2]
                #except:
                #        pass

		try:
			return wikilangdata[skill1][skill2]
		except:
			pass
	
		try:
			return wiki_tfidfdata[skill1][skill2]
		except:
			pass

		return 0.0

	#skill_total = list(set(solargedata.keys() + mathselargedata.keys() + wikilangdata.keys() + wiki_tfidfdata.keys() + soquantlargedata.keys() + soeleclargedata.keys()))
	skill_total = list(set(solargedata.keys() + mathselargedata.keys() + wikilangdata.keys() + wiki_tfidfdata.keys() + soquantlargedata.keys()))

	execfile("skill_list.py")
	skill_total = filter(lambda x: x in skill_list, skill_total)
	
	outputdict = {}
        for skill in skill_total:
                outputdict[skill] = {}

	for comb in itertools.permutations(skill_total,2):
                outputdict[comb[0]][comb[1]] = getMerged(comb[0], comb[1])

        print outputdict
        with open('result.txt', 'w') as infile:
                infile.write(json.dumps(outputdict))

	manual_overridden_outputdict = modifyManualInput(outputdict)
	
	manual_overridden_forced_output = modifyManualInputForced(outputdict)
	skill_total_forced = manual_overridden_forced_output['skills']
	manual_overridden_forced_outputdict = manual_overridden_forced_output['outputdict']

	with open('manual_overridden_result.txt', 'w') as infile:
        	infile.write(json.dumps(manual_overridden_forced_outputdict))	

        execfile("floyd-warshall.py")
        completematrix=floydwarshall(manual_overridden_outputdict, skill_total_forced)
        with open('complete.txt', 'w') as infile:
                infile.write(json.dumps(completematrix))

if sys.argv[1] == "diffresults":
	getDiff('so-large/result.txt', 'so-large/resultold.txt', 'so-large/diff.txt')
	getDiff('mathse-large/result.txt', 'mathse-large/resultold.txt', 'mathse-large/diff.txt')
	getDiff('so-quant-large/result.txt', 'so-quant-large/resultold.txt', 'so-quant-large/diff.txt')
	#getDiff('so-elec-large/result.txt', 'so-elec-large/resultold.txt', 'so-elec-large/diff.txt')
	getDiff('wikilang/result.txt', 'wikilang/resultold.txt', 'wikilang/diff.txt')
	getDiff('wiki_tfidf/result.txt', 'wiki_tfidf/resultold.txt', 'wiki_tfidf/diff.txt')
	getDiff('result.txt', 'resultold.txt', 'diff.txt')

if sys.argv[1] == "getrenamedresults":
	getRenamed('so-large/result.txt', 'so-large/renamedresult.txt')
	getRenamed('mathse-large/result.txt', 'mathse-large/renamedresult.txt')
	getRenamed('so-quant-large/result.txt', 'so-quant-large/renamedresult.txt')
	getRenamed('so-elec-large/result.txt', 'so-elec-large/renamedresult.txt')
	getRenamed('wikilang/result.txt', 'wikilang/renamedresult.txt')
	getRenamed('wiki_tfidf/result.txt', 'wiki_tfidf/renamedresult.txt')
	getRenamed('result.txt', 'renamedresult.txt')
	getRenamed('manual_overridden_result.txt', 'manual_overridden_renamedresult.txt')
	






