import json

def readJson(path):
	file = open(path,'r')
	return json.load(file)


