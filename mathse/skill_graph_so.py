import urllib2
import math
import itertools
import functools32
import gevent
from gevent import monkey
from gevent.pool import Pool

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
    if getNumQues(skill)<=100:
	return 0
    else:
	return 1
    
def getSOhtml2(skill1, skill2):
    try:
	f = open('htmldump/' + skill1 + skill2, 'r')
	data = f.read()
	f.close()
    except:
	filedata = urllib2.urlopen("http://math.stackexchange.com/questions/tagged/"+skill1+"+"+skill2)
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
        filedata = urllib2.urlopen("http://math.stackexchange.com/questions/tagged/"+skill)
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
        
	skill=html5[:html5.find("<")]
	num6=html5.find('<span class="item-multiplier-count">')
        parentques=getNumQues(skill)
	html6=html5[num6+36:]
	commonques=html6[:html6.find("<")]
	if len(skill.strip())>0:
		resultcommonques.update({skill:float(commonques)})
		resultparentques.update({skill:float(parentques)})
		resultnumques.update({skill:float(numques)})
		if parentques > numques:
			summation+=float(commonques)
    return { 'summation': summation, 'commonques': resultcommonques, 'parentques': resultparentques, 'numques': resultnumques }

def prob_A_given_B(skill1, skill2):
    parentinfodict = getParentInfo(skill1)
    summation = parentinfodict['summation']
    
    #print "Sum: " + str(summation)
    #print "Base: " + str(parentinfo[skill2])
    #print skill1+" given "+ skill2 + " " + "{0:.2f}".format(parentinfo[skill2]/summation)
    try:
	retval =  float(parentinfodict['commonques'][skill2])/float(parentinfodict['parentques'][skill2])
	retval = (7.0/11.0)*math.atan(retval*10000.0/300.0)
    except Exception as e:
	#print "Exception: " + skill1 + " " + skill2 + " " + str(e.args)
	retval = 0.0

    try:
	print skill1 + " " + skill2 + " " + str(parentinfodict['commonques'][skill2]) + " " + str(parentinfodict['parentques'][skill2]) + " " + str(parentinfodict['numques'][skill2]) + " " + str(summation) + " = " + str("{0:.2f}".format(retval))
    except:
	pass

    return retval


skills = ["Machine Learning", "Probability", "Statistics", "Data Mining", "NLP", "Hadoop", "Programming", "SQL", "Algorithm", "Artificial Intelligence", "Pattern Recognition", "Python", "Django", "C++", "Java", "Ruby", "Algebra", "Convex Optimization", "Optimization"]
skills = map(lambda x: slugify(x), skills)
skills2 = filter(lambda x: check_skill_so(x), skills) 
print skills2

## Save all the files
#pool = Pool(len(skills2))
#jobs = [pool.spawn(getParentInfo, skill) for skill in skills2]
#pool.join()

outputdict = {}
for skill in skills2:
	outputdict[skill] = {}

for comb in itertools.permutations(skills2,2):
	val = prob_A_given_B(comb[0], comb[1])
	outputdict[comb[0]][comb[1]] = val


print outputdict
printMatrix(skills, outputdict)






