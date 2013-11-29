import urllib2
import sys
import json

skill_list_dmoz_lang = ['abap', 'abc', 'ada', 'adl', 'algol-60', 'algol-68', 'apl', 'applescript', 'arb', 'assembly', 'awk', 'basic', 'befunge', 'beta', 'bigwig', 'bistro', 'blue', 'brainfuck', 'c', 'c++', 'caml', 'cecil', 'cg', 'chill', 'clarion', 'clean', 'clipper', 'clojure', 'clu', 'cobol', 'cobolscript', 'cocoa', 'component-pascal', 'c-sharp', 'curl', 'd', 'databus', 'delphi', 'dos-batch', 'dylan', 'e', 'eiffel', 'elastic', 'erlang', 'euphoria', 'forth', 'fortress', 'fp', 'frontier', 'glsl', 'goedel', 'groovy', 'haskell', 'hlsl', 'html', 'htmlscript', 'hypercard', 'ici', 'icon', 'idl', 'intercal', 'io', 'jal', 'java', 'javascript', 'jovial', 'labview', 'lagoona', 'latex', 'leda', 'limbo', 'lisp', 'logo', 'lua', 'm4', 'maple', 'mathematica', 'matlab', 'mercury', 'miranda', 'miva', 'ml', 'modula-2', 'modula-3', 'moto', 'mumps', 'oberon', 'objective-caml', 'objective-c', 'obliq', 'occam', 'oz', 'pascal', 'perl', 'php', 'pike', 'pl', 'pliant', 'pl-sql', 'pop-11', 'postscript', 'powerbuilder', 'prograph', 'prolog', 'proteus', 'python', 'r', 'rebol', 'refal', 'rexx', 'rigal', 'rpg', 'ruby', 'sas', 'sather', 'scheme', 'self', 'setl', 'sgml', 'simkin', 'simula', 'sisal', 's-lang', 'smalltalk', 'snobol', 'sql', 'squeak', 't3x', 'tads', 'tcl-tk', 'tempo', 'tex', 'tom', 'trac', 'transcript', 'turing', 'uml', 'vbscript', 'verilog', 'vhdl', 'visual-basic', 'visual-dialogscript', 'visual-foxpro', 'water', 'xml', 'xotcl', 'yafl', 'yorick', 'z']


def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

def getParents(skill):
    try:
	    data = urllib2.urlopen("http://www.dmoz.org/search?cat=Computers%2FProgramming%2FLanguages&all=no&q="+skill)
	    html = data.read()
	    html2=html[html.find('<ol class="dir" start=1>'):]
	    html3=html2[html2.find('<a href="')+9:]
	    html4=html3[:html3.find('"')]
	    html5=html4[html4.find("/Computers/Programming/Languages/")+33:]
	    html6=html5[:html5.find('/')]
	    if html6:
		    html6 = slugify(html6)
		    if html6 in skill_list_dmoz_lang:
			    print skill + " - " + html6
			    return html6
	    else:
		return None
    except:
    	    return None

getParents("django")
getParents("python")
getParents("mootools")
getParents("jquery")
getParents("ruby")
getParents("rails")
getParents("dojo")

def prob_A_given_B(skill1, skill2):
	try:
		parent1 = getParents(skill1).lower()
		parent2 = getParents(skill2).lower()
		if parent1==skill2:
			return 0.98
		else:
			return None
	except:
		return None

prob_A_given_B("django","python")
prob_A_given_B("jquery","javascript")

if not len(sys.argv) == 2:
	print "Usage : python skill_graph_dmoz.py saveresults"
	sys.exit(1)

if sys.argv[1] not in ["saveresults"]:
	print "Usage : python skill_graph_dmoz.py saveresults"
	sys.exit(1)

skills = ["Machine Learning", "Probability", "Statistics", "Data Mining", "NLP", "Hadoop", "Programming", "SQL", "Algorithm", "Artificial Intelligence", "Pattern Recognition", "Python", "Django", "C++", "Java", "Ruby", "Algebra", "Convex Optimization", "Optimization"]
execfile("../skill_list.py")
skills = skill_list
skills2 = map(lambda x: slugify(x), skills)
print skills2

if sys.argv[1] == "saveresults":
	outputdict = {}
	for skill in skills2:
		outputdict[skill] = {}

	for skill in skills2:
		skill_parent = getParents(skill)
		if skill_parent in skills2:
			outputdict[skill_parent][skill] = 0.98				

	print outputdict
	with open('result.txt', 'w') as infile:
		infile.write(json.dumps(outputdict))


