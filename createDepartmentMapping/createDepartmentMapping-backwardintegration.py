import json
import urllib2

def getSkillsfromTagGraph(skillfile):
        with open(skillfile, 'r') as infile:
            data=json.load(infile)
        return data.keys()

def getSkillsfromDepartmentMapping(skillfile):
        with open(skillfile, 'r') as infile:
            data=json.load(infile)
        return data.keys()


def getSkillsFromDepartmentMappingLink(googledocid, outputfile='manualdepartmentmapping.txt'):

	print 'https://spreadsheets.google.com/feeds/list/'+googledocid+'/od6/public/basic?hl=en_US&alt=json'
	d = json.load(urllib2.urlopen('https://spreadsheets.google.com/feeds/list/'+googledocid+'/od6/public/basic?hl=en_US&alt=json'))
	output = {}

	for entry in d['feed']['entry']:
        	try:
			s = entry['content']['$t']
			a = map(lambda x: x.strip().split(':')[1].strip(), s.split(','))
                	output[entry['title']['$t']] = [tuple(a[i:i+2]) for i in range(0, len(a), 2)]
	        except:
        	        pass

	with open(outputfile, 'w') as infile:
                infile.write(json.dumps(output))
	return output.keys()

def createDepMapping(skillfiletocheck, googledocidtocheck):
	l1 = getSkillsfromTagGraph(skillfiletocheck)
	l2 = getSkillsFromDepartmentMappingLink(googledocidtocheck, outputfile=skillfiletocheck+'-manualdepartmentmapping.txt')
	print "Skills to be removed from Mapping File"
	for i in  sorted(list(set(l2)-set(l1))):
		print i
	print "Skills to be added to Mapping File"
	for i in sorted(list(set(l1)-set(l2))):
		print i
	return

createDepMapping('V1.0_tag_graph_data.txt', '0Ang7Vqp7FIPSdEFMN0UxbU1EWkdrbG1nbThnRU5jd3c')
createDepMapping('V2.0_tag_graph_data.txt', '0Ang7Vqp7FIPSdFJnR2hKeXBXRmowX0hveDk3cWxYZXc')
createDepMapping('V3.0_tag_graph_data.txt', '0AjPfOfZ0QaixdGEzZ2djdHJRVFgtR3pZejhVQlZnSEE')

l1 = sorted(getSkillsfromTagGraph('V1.0_tag_graph_data.txt')) 
l2 = sorted(getSkillsfromTagGraph('V2.0_tag_graph_data.txt'))
l3 = sorted(getSkillsfromTagGraph('V3.0_tag_graph_data.txt'))
p1 = sorted(getSkillsfromDepartmentMapping('V1.0_tag_graph_data.txt-manualdepartmentmapping.txt'))
p2 = sorted(getSkillsfromDepartmentMapping('V2.0_tag_graph_data.txt-manualdepartmentmapping.txt'))
p3 = sorted(getSkillsfromDepartmentMapping('V3.0_tag_graph_data.txt-manualdepartmentmapping.txt'))

