import urllib2
from bs4 import BeautifulSoup
import re

output = {}

def getCourseContents(link, name):
	html = urllib2.urlopen(link).read()
	bs = BeautifulSoup(html)

        try:
                if name not in output.keys():
                        rows = bs.find_all('td', attrs = {'headers': 'col4'})
                        o = []
                        for x in rows:
                                try:
                                        o.append(str(x))
                                except:
                                        pass
                        if o:
                                output[name] = o
        except:
                pass

	try:
		if name not in output.keys():
			rows = bs.find_all('tr', attrs = {'class':re.compile(r'^row$|^alt-row$')})
			o = []
			for x in rows:
				try:
					o.append(x.find_all('td')[1])
				except:
					pass
			if o:
				output[name] = o
	except:
		pass

	print name
	print output[name]
	print "--"
	return

	
getCourseContents("http://ocw.mit.edu/courses/physics/8-02-physics-ii-electricity-and-magnetism-spring-2007/class-topics/", "Physics II: Electricity and Magnetism")
getCourseContents("http://ocw.mit.edu/courses/mechanical-engineering/2-00aj-exploring-sea-space-earth-fundamentals-of-engineering-design-spring-2009/study-materials/", "Exploring Sea, Space, & Earth: Fundamentals of Engineering Design")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-00-introduction-to-aerospace-engineering-and-design-spring-2003/calendar/", "Introduction to Aerospace Engineering and Design")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-050-thermal-energy-fall-2002/calendar/", "Thermal Energy")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-06-principles-of-automatic-control-fall-2003/calendar/", "Principles of Automatic Control")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-07-dynamics-fall-2009/calendar/", "Dynamics")
getCourseContents("http://ocw.mit.edu/courses/aeronautics-and-astronautics/16-100-aerodynamics-fall-2005/calendar/", "Aerodynamics")





