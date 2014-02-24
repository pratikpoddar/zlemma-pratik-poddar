#!/usr/bin/python
import json
import sys
import urllib
import urllib2
import re
import nltk
import requests
from bs4 import BeautifulSoup
import time
import pickle

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def get_closest_stackoverflow_tag(word):
	try:
		#bs = BeautifulSoup(requests.get('http://www.stackoverflow.com/questions/tagged/' + word).text)
		#rt = BeautifulSoup(bs.find_all('', {'class': 'js-gps-related-tags'})[0].text())
		#return rt.find_all('', {'class':'post-tag'})[0].text()

		return requests.get('https://api.stackexchange.com/2.2/tags/'+word+'/related?site=stackoverflow&key=820vG6UjV1aqh8wdyEUNeA((').json()['items'][0]['name']
	except:
		return None

def get_semantic_link_related(word):
	return map(lambda x: x['v'], requests.get("http://www.semantic-link.com/related.php?word="+word).json()[:5])

def get_freebase_related(term):
	def get_Freebase_Meaning(term):

        	try:
                	url = "https://www.googleapis.com/freebase/v1/search?key=AIzaSyCIeO8t4Su2hM0hm8t3aGCgiApBLu7MvGE&query=" + urllib.quote_plus(term)
	                jsonResult = json.loads(urllib2.urlopen(url).read())['result']
	                if jsonResult:
        	                if jsonResult[0]['score']>10:
                	                try:
                        	                return {'parentnode': jsonResult[0]['notable']['name'], 'wikilink': jsonResult[0]['id'], 'title': jsonResult[0]['name'], 'parentlink': jsonResult[0]['notable']['id']}
	                                except:
						raise
                	        else:
                        	        return None
	                else:
        	                return None
	        except Exception as e:
        	        return None

	def get_Freebase_Children(query):

		try:
			service_url = "https://www.googleapis.com/freebase/v1/mqlread?"
			api_key = "AIzaSyCIeO8t4Su2hM0hm8t3aGCgiApBLu7MvGE"
			query = [{'id': None, 'name': None, 'type': query}]
			params = {
		        'query': json.dumps(query),
        		'key': api_key
			}
			output = []
			url = service_url + urllib.urlencode(params)
			response = json.loads(urllib.urlopen(url).read())
			for r in response['result']:
				output.append(r['name'])

			return output
		except:
			pass

	try:
		return get_Freebase_Children(get_Freebase_Meaning(term)['parentlink'])
	except:
		return None

def getData(filename):
        with open(filename, 'r') as infile:
            data=json.load(infile)
        return data


def getAllTags():

	try:
		file = open('stackoverflowalltags.txt', 'r')
		alltags = pickle.load(file)
		file.close()
		alltags = list(set(alltags))
		if alltags:
			print "All Tags file already exisits"
			print len(alltags)
			return alltags
		else:
			raise
		
	except:
		alltags = []
		print "All Tags file does not exist"
		for i in range(1055):
			alltags += map(lambda x: x.text, BeautifulSoup(requests.get("http://stackoverflow.com/tags?page="+str(i)+"&tab=name").text).find_all('',{'class':'post-tag'}))
		alltags = list(set(alltags))
		file = open('stackoverflowalltags.txt', 'w')
		pickle.dump(alltags, file)
		file.close()
		alltags = list(set(alltags))
		print len(alltags)
		return alltags


def initializeClosestMapDictionary(allsotags):

        try:
                file = open('stackoverflowtagalias.txt', 'r')
                sooutput = pickle.load(file)
                file.close()
                if sooutput.items():
			print "StackoverFlow Tag Alias file already exists"
			print len(sooutput.items())
			print len(filter(lambda x: not ((x[1]==None) or (x[1]=='')), sooutput.items()))
                        return sooutput
                else:
                        raise

        except:
		print "Stackoverflow tag alias file does not exist"
                sooutput = {}
		for tag in allsotags:
		        sooutput[tag] = None
                file = open('stackoverflowtagalias.txt', 'w')
                pickle.dump(sooutput, file)
                file.close()
                print len(sooutput.items())
                print len(filter(lambda x: not ((x[1]==None) or (x[1]=='')), sooutput.items()))
                return sooutput


def findClosestTag(sooutput, alltags, alias):

	output = sooutput[alias]
	counter = 0
	while 1:
		counter+=1
		if output in alltags:
			return output
		if output == alias:
			return None
		if output == None:
			return None
		if output == '':
			return None
		if counter == 50:
			print "findClosestTag failed for " + alias
			return None
		output = sooutput[output]

	return None

#terms = getData('renamedcomplete.txt').keys()
#output = []
#for term in terms:
#	sl = get_semantic_link_related(term)
#	fb = get_freebase_related(term)
#	print (term, sl, fb)
#	output.append((term, sl, fb))
	
#import pickle
#file = open('tagalias_fb_sl.txt', 'w')
#pickle.dump(output, file)
#file.close()

allsotags = list(set(getAllTags()))
sooutput = initializeClosestMapDictionary(allsotags)

counter = 0
for pair in sooutput.items():
	counter += 1
	if pair[1] == None or pair[1] == '':
		sooutput[pair[0]] = get_closest_stackoverflow_tag(pair[0])
	if counter==500:
		counter = 0
		file = open('stackoverflowtagalias.txt', 'w')
		pickle.dump(sooutput, file)
		file.close()
		print "stackoverflowtagalias.txt file saved - counter " + str(counter)

file = open('stackoverflowtagalias.txt', 'w')
pickle.dump(sooutput, file)
file.close()

print "stackoverflowtagalias.txt file saved - finally "

soclosesttag = {}
for alias in sooutput.keys():
	soclosesttag[alias] = findClosestTag(sooutput, allsotags, alias)

file = open('stackoverflowtagaliasfinal.txt', 'w')
pickle.dump(soclosesttag, file)
file.close()




