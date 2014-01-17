import urllib2
import math
import itertools
import functools32
import sys
import gevent
import json
from BeautifulSoup import BeautifulSoup
import pickledb
import gevent
from gevent import monkey
from gevent.pool import Pool
import json
#from tor_urllib2 import getUrl

monkey.patch_all(thread=False)

db = pickledb.load('microsoft-search.db', False)

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

def getMSdata(skill):
    try:
	f = open('htmldump/' + skill, 'r')
	data = f.read()
	f.close()
	print "Found skill " + skill + " from file"
    except:
	print "Could not get " + skill + " data"
    return data

def getorcreateMSdata(kwid):
	print "getorcreateMSdata " + str(kwid)
	try:
		return getMSdata(db.get(kwid))
	except:
		try:
			print kwid
			opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(), urllib2.ProxyHandler({'http':'127.0.0.1:8118'}))
                	opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'), ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]
			url = "http://academic.research.microsoft.com/Keyword/"+str(kwid)
			print url
                	filedata = opener.open(url)
			data = filedata.read()
			###### data = getUrl(url)
			print str(kwid) + "------" + data[0:100]
			parsed = BeautifulSoup(data)
			if parsed.title.text:
				print 'htmldump/' + slugify(str(parsed.title.text))
				f = open('htmldump/' + slugify(str(parsed.title.text)), 'w')
				f.write(data)
				f.close()
				db.set(kwid, slugify(str(parsed.title.text)))
				db.dump()
				return data
		except Exception as e:
			print "Could not save " + str(kwid) + " - " + str(e)
			raise


def getKeywordData(skill):
	data = getMSdata(skill)
	parsed = BeautifulSoup(data)
	keywords = str(filter(lambda x: str(x).find('var _keyword_data')>0, parsed.findAll('script'))[0].text).replace('//<![CDATA[','').replace('//]]>','').replace('\r\n','').strip().replace('var _keyword_data = ','').replace('[','').replace('];','').split(',')
	return keywords


if sys.argv[1] == "downloaddata":
	#getorcreateMSdata(int(sys.argv[2]))
	#for i in range(1,100):
	#	getorcreateMSdata(i)
	for i in range(2, 100):
		pool = Pool(200)
		jobs = [pool.spawn(getorcreateMSdata , n) for n in range(i*200,(i+1)*200)]
		pool.join()

