import urllib2
import math
import itertools
import functools32
import sys
import gevent
from gevent import monkey
from gevent.pool import Pool
import json

monkey.patch_all(thread=False)

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

def printMatrix(skills, outputdict):
        skillset = []
        for skillx in skills:
                for skilly in skills:
                        try:                    
                                if outputdict[skillx][skilly] > 0.02:
                                        skillset.append(skillx)
                                        skillset.append(skilly)
                        except:
                                pass
        skills = list(set(skillset))

        row = '\t'
        for skillx in skills:
                row += skillx + '\t'
        print row

        for skilly in skills:
                row = skilly + '\t'
                for skillx in skills:
                        try:
                                if outputdict[skillx][skilly] < 0.02:
                                        row += str("")+'\t'
                                else:
                                        row += str("{0:.2f}".format(outputdict[skillx][skilly]))+'\t'
                        except Exception as e:
                                row += str("")+'\t'
                print row

	return

def check_skill_so(skill):
    if getNumQues(skill)<=10:
	return 0
    else:
	return 1
    
def getSOhtml2(skill1, skill2):
    try:
	f = open('htmldump/' + skill1 + skill2, 'r')
	data = f.read()
	f.close()
    except:
	filedata = urllib2.urlopen("http://www.stackoverflow.com/questions/tagged/"+skill1+"+"+skill2)
	data = filedata.read()
	f = open('htmldump/' + skill1 + skill2, 'w')
	f.write(data)
	f.close()
    return data

def getSOhtml1(skill):
    try:
        f = open('htmldump/' + skill, 'r')
        data = f.read()
        f.close()
    except:
        filedata = urllib2.urlopen("http://www.stackoverflow.com/questions/tagged/"+skill)
        data = filedata.read()
        f = open('htmldump/' + skill, 'w')
        f.write(data)
        f.close() 
    return data

@functools32.lru_cache(maxsize=32)
def getNumQues(skill):
    try:
	html = getSOhtml1(skill)
   	numques = getNumQuesHTML(getSOhtml1(skill))
    except:
	numques = 1
    return numques

def getNumQuesHTML(html):
    num=html.find('<div class="summarycount al">')
    html2=html[num+29:]
    num2=html2.find("<")
    output= html2[0:num2]
    try:
	return float(output.replace(",",""))
    except:
	print "Exception" + output + "----" + str(num2)
	return 1

@functools32.lru_cache(maxsize=32)
def getParentInfo(skill):
	try:
		html = getSOhtml1(skill)
		numques = int(getNumQues(skill))
		num=html.find('<h4 id="h-related-tags">Related Tags</h4>')
		html2=html[num+41:]
		num2=html2.find('<\div>')
		html3=html2[:num2]
		num3=1
		result={}
		resultcommonques={}
		resultparentques={}
		resultnumques={}
		summation = 0.0
		while num3>0:
			num3=html3.find('<a href="/questions/tagged/')
			html4=html3[num3+27:]
			num4=html4.find(">")
			html5=html4[num4+1:]
			num5=html5.find("<br>")
			html3=html5[num5+4:]
	
			skill2=html5[:html5.find("<")]
			parentques=getNumQues(skill2)
			try:
				num6=html5.find('<span class="item-multiplier-count">')
				html6=html5[num6+36:]
				commonques=html6[:html6.find("<")]
				commonques=float(commonques)
			except:
				commonques=float(0.0)
		
			if len(skill2.strip())>0:
				resultcommonques.update({skill2:float(commonques)})
				resultparentques.update({skill2:float(parentques)})
				resultnumques.update({skill2:float(numques)})
				if parentques > numques:
					summation+=float(commonques)

		return { 'summation': summation, 'commonques': resultcommonques, 'parentques': resultparentques, 'numques': resultnumques }

	except Exception as e:
		print "Error: " + skill 
		print e
		return { 'summation': 0, 'commonques': 0, 'parentques': 0, 'numques': 0 }

def prob_A_given_B(skill1, skill2):
    parentinfodict = getParentInfo(skill1)
    summation = parentinfodict['summation']
    
    #print "Sum: " + str(summation)
    #print "Base: " + str(parentinfo[skill2])
    #print skill1+" given "+ skill2 + " " + "{0:.2f}".format(parentinfo[skill2]/summation)
    try:
	if float(parentinfodict['commonques'][skill2]) > 3:
		retval = float(parentinfodict['commonques'][skill2])/float(parentinfodict['parentques'][skill2])
		retval = (7.0/11.0)*math.atan(retval*10000.0/300.0) 
	else:
		retval = 0.0
    except Exception as e:
	#print "Exception: " + skill1 + " " + skill2 + " " + str(e.args)
	retval = 0.0

    try:
	print skill1 + " " + skill2 + " " + str(parentinfodict['commonques'][skill2]) + " " + str(parentinfodict['parentques'][skill2]) + " " + str(parentinfodict['numques'][skill2]) + " " + str(summation) + " = " + str("{0:.2f}".format(retval))
    except:
	pass

    return retval

#if not len(sys.argv) == 2:
	#print "Usage : python skill_graph_so.py [downloaddata | saveresults]"
	#sys.exit(1)

#if sys.argv[1] not in ["downloaddata","saveresults"]:
#	print "Usage : python skill_graph_so.py [downloaddata | saveresults]"
#	sys.exit(1)

skills = ["Machine Learning", "Probability", "Statistics", "Data Mining", "NLP", "Hadoop", "Programming", "SQL", "Algorithm", "Artificial Intelligence", "Pattern Recognition", "Python", "Django", "C++", "Java", "Ruby", "Algebra", "Convex Optimization", "Optimization"]
execfile("../skill_list.py")
skills = skill_list
skills = map(lambda x: slugify(x), skills)
skills2 = filter(lambda x: check_skill_so(x), skills)
print skills2

if sys.argv[1] == "downloaddata":
	## Save all the files
	pool = Pool(len(skills2))
	jobs = [pool.spawn(getParentInfo , skill) for skill in skills2]
	pool.join()

if sys.argv[1] == "saveresults":
	outputdict = {}
	for skill in skills2:
		outputdict[skill] = {}

	print skills2

	for comb in itertools.permutations(skills2,2):
		val = prob_A_given_B(comb[0], comb[1])
		outputdict[comb[0]][comb[1]] = val

	print outputdict
	printMatrix(skills, outputdict)
	with open('result.txt', 'w') as infile:
		infile.write(json.dumps(outputdict))

	execfile("../floyd-warshall.py")
	completematrix=floydwarshall(outputdict, skills)
	with open('complete.txt', 'w') as infile:
		infile.write(json.dumps(completematrix))


