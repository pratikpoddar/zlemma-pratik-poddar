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

def camelCase(word):
    if word:
        return ' '.join(x[0].upper()+x[1:] for x in word.split('-'))
    else:
        return None

def mergeSkills(pathold, pathnew):

	merge_replacements = getData('manualreplacements.txt')

	outputDict = getData(pathold)
	newOutputDict = {}
	
	for kv in outputDict.items():
	    try:
	        merge_v = merge_replacements[kv[1]]
	    except:
	        merge_v = kv[1]
	        
	    newOutputDict[kv[0]]  = merge_v
	    
	with open(pathnew, 'w') as infile:
	    infile.write(json.dumps(newOutputDict))
	    
	return

def getCamelCased(pathold, pathrenamed):
	
    outputDict = getData(pathold)
    newOutputDict = {}

    for key in outputDict.keys():
        newOutputDict[camelCase(key)] = camelCase(outputDict[key])

    with open(pathrenamed, 'w') as infile:
        infile.write(json.dumps(newOutputDict))
        
    return

def getRenamed(pathold, pathnew):
	getCamelCased(pathold, pathnew)
	mergeSkills(pathnew, pathnew)
	return


