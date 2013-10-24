import urllib2

def getParents(skill):
    data = urllib2.urlopen("http://www.dmoz.org/search?cat=Computers%2FProgramming%2FLanguages&all=no&q="+skill)
    html = data.read()
    html2=html[html.find('<ol class="dir" start=1>'):]
    html3=html2[html2.find('<a href="')+9:]
    html4=html3[:html3.find('"')]
    html5=html4[html4.find("/Computers/Programming/Languages/")+33:]
    html6=html5[:html5.find('/')]
    print skill + " - " + html6
    return

getParents("django")
getParents("python")
getParents("mootools")
getParents("jquery")
getParents("ruby")
getParents("rails")
getParents("dojo")

def prob_A_given_B(skill1, skill2):
	parent1 = getParents(skill1).lower()
	parent2 = getParents(skill2).lower()
	if parent1==skill2:
		return 0.98
	if parent2==skill1:
		return 0.6
	else:
		return 0.0

	
prob_A_given_B("django","python")
prob_A_given_B("jquery","javascript")





