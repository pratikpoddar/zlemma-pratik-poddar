import urllib2
from bs4 import BeautifulSoup
import re
import urllib
import json

output = {}

blocked_wiki = [ '/en/hot_r_b_hip_hop_songs', '/en/gain', '/en/u_s_open', '/en/first-class_cricket', '/en/workers_compensation', '/en/news', '/en/design', '/en/engineering_ethics', '/en/dell_xps' ]

def get_Freebase_Meaning(term):

        try:
                url = "https://www.googleapis.com/freebase/v1/search?key=AIzaSyCIeO8t4Su2hM0hm8t3aGCgiApBLu7MvGE&query=" + urllib.quote_plus(term)
                jsonResult = json.loads(urllib2.urlopen(url).read())['result']
                if jsonResult:
                        if jsonResult[0]['score']>150:
                        	return {'node': jsonResult[0]['name'], 'wikilink': jsonResult[0]['id']}
                        else:
                                return None
                else:
                        return None
        except Exception as e:
		print e
                return None

def cleantext(text):
	text1 = text.lower()
	text1 = text1.replace('introduction to', '')
	text1 = text1.replace('fundamentals of', '')
	text1 = re.sub(r'lec #\d+:', ' ', text1)
	elems = text1.split('\n')
	elems2 = []
	for elem in elems:
		if len(elem.strip())>0:
			if not filter(lambda x: elem.lower().find(x) > -1, ['notes', 'introductory', 'exam', 'holiday', 'team', 'conclusion', 'quiz', 'oral', 'final topics', 'midterm', '(cont.)', 'guest', ' day', 'working in groups', 'poster', 'lab']):
				elems2.append(elem.strip())
	text2 = ', '.join(elems2)
	print "---"
	print "text:"
	print text
	wikielems = []
	if text2:
		#print text2
		elems = re.split(r'[;,]|and', text2)
		for elem in elems:
			try:
				wikielem =  get_Freebase_Meaning(elem)
				#print wikielem
				if wikielem['wikilink']:
					if wikielem['wikilink'].find('/en/') > -1:
						if wikielem['wikilink'] not in blocked_wiki:
							wikielems.append((wikielem['wikilink'], wikielem['node']))
						
			except:
				pass
	if wikielems:
		print "wikielems:"
		print ', '.join(map(lambda x: x[0]+";;"+x[1], wikielems))
		print "---"
		return ', '.join(map(lambda x: x[0]+";;"+x[1], wikielems))
	else:
		print "---"
		return None

def strip_tags(text):
	return re.sub('<[^<]+?>', '', text)

def getCourseContents(link):
	html = urllib2.urlopen(link).read()
	bs = BeautifulSoup(html)

        try:
                if link not in output.keys():
                        rows = bs.find_all('td', attrs = {'headers': 'col4'})
                        o = []
                        for x in rows:
                                try:
                                        o.append(str(x))
                                except Exception as e:
                                        pass
                        if o:
				#print o
				try:
	                                output[link] = map(lambda x: cleantext(strip_tags(str(x))), o)
				except Exception as e:
					print e
        except:
                pass

	try:
		if link not in output.keys():
			rows = bs.find_all('tr', attrs = {'class':re.compile(r'^row$|^alt-row$')})
			o = []
			for x in rows:
				try:
					o.append(x.find_all('td')[1])
				except Exception as e:
					pass
			if o:
				#print o
				try:
					output[link] = map(lambda x: cleantext(strip_tags(str(x))), o)
				except Exception as e:
					print e
	except:
		pass

	return

	

getCourseContents("http://ocw.mit.edu/courses/physics/8-02-physics-ii-electricity-and-magnetism-spring-2007/class-topics/")
getCourseContents("http://ocw.mit.edu/courses/mechanical-engineering/2-00aj-exploring-sea-space-earth-fundamentals-of-engineering-design-spring-2009/study-materials/")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-00-introduction-to-aerospace-engineering-and-design-spring-2003/calendar/")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-050-thermal-energy-fall-2002/calendar/")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-06-principles-of-automatic-control-fall-2003/calendar/")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-07-dynamics-fall-2009/calendar/")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-100-aerodynamics-fall-2005/calendar/")
getCourseContents("http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-046j-design-and-analysis-of-algorithms-spring-2012/calendar/")
getCourseContents("http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-005-elements-of-software-construction-fall-2011/calendar/")

import pickle
with open('bubnaocwdump2.pickle', 'w') as f:
    pickle.dump(output, f)


