from sklearn.feature_extraction.text import TfidfVectorizer
import lxml
from lxml import html
from feedreader.parser import from_url

def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
def removeNonAsciiIgnore(s):
	try:
		return removeNonAscii(str(s))
	except:
		return ""

def pairwiseSimilarity(documents):

	documents = map(lambda x: removeNonAscii(x), documents)
	tfidf = TfidfVectorizer(min_df=1).fit_transform(documents)
	pairwise_similarity = tfidf * tfidf.T
	return pairwise_similarity


def getAllBlogArticles(url):

	response = {}
	parsedblog = from_url(url)
	response['title'] = parsedblog.title
	response['titles'] = map(lambda x: x.title, parsedblog.entries)
	response['articles'] = map(lambda x: lxml.html.fromstring(x.description).text_content().replace('\n', ' '), parsedblog.entries)
	response['authors'] = map(lambda x: x.author.name if x.author else "" , parsedblog.entries)
	return response

def getAllBlogs():

	titles = []
	articles = []
	authors = []
	urls = []
	urls.append("http://feeds.feedburner.com/pratikpoddarcse")
	urls.append("http://feeds.feedburner.com/Techcrunch")
	blogs = map(lambda x: getAllBlogArticles(x), urls)
	for blog in blogs:
		print blog['title']
		titles += map(lambda x: removeNonAsciiIgnore(x), blog['titles'])
		articles += map(lambda x: removeNonAscii(x), blog['articles'])
		authors += map(lambda x: removeNonAsciiIgnore(x), blog['authors'])

	print len(titles)
	print len(articles)
	print len(authors)
	documents = map(lambda x: ' '.join(x), zip(titles, authors, articles))
	print len(documents)
	return documents

documents = getAllBlogs()
print "Number of documents: " + str(len(documents))
pwsim_result = pairwiseSimilarity(documents)



