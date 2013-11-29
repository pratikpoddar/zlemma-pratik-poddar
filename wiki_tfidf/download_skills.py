from wikipedia_extractor import Wikipedia, Wiki2Plain
import urllib
from tfidf import pairwiseSimilarity
import sys
import json

def slugify(title):
    name = title.replace(' ', '-').lower()
    return name

def download_page_from_wiki(skill):
    print "Download Page from Wiki " + skill
    wiki = Wikipedia('en')
    try:
        skill_content = wiki.article(skill)
    except Exception as e:
	print "Exception " + skill + " " + str(e)
        skill_content = None

    if skill_content:
	if skill_content.lower().find("disambig") == -1:
        	skill_content_plain = Wiki2Plain(skill_content)
	        content = skill_content_plain.text
        	with open("dump/"+skill+".txt", "w") as text_file:
	            text_file.write(content)
		print "Created file dump/" + skill + ".txt"
	else:
		print "Disambiguation needed for skill " + skill + ". Please visit " + "http://en.wikipedia.org/w/index.php?action=raw&title=" + skill

    return

def check_if_downloaded(skill):
    try:
        with open("dump/"+skill+".txt","r") as text_file:
            content = text_file.read()
        return content
    except:
	return 0

def save_page(skill):
    if not check_if_downloaded(skill):
        download_page_from_wiki(skill)
    return
    

if not len(sys.argv) == 2:
        print "Usage : python download_skills.py [downloaddata | saveresults]"
        sys.exit(1)

if sys.argv[1] not in ["downloaddata","saveresults"]:
        print "Usage : python download_skills.py [downloaddata | saveresults]"
        sys.exit(1)

execfile("../skill_list.py")
skill_list = map(lambda x: x.replace("-", " "), skill_list)
skill_list = map(lambda x: slugify(x), skill_list)
print skill_list

if sys.argv[1] == "downloaddata":
	for skill in skill_list:
		save_page(skill)

if sys.argv[1] == "saveresults":
    documents = []
    skillset = []
    for skill in skill_list:
        try:
            content = check_if_downloaded(skill)
	    if content:
                documents.append(content)
                skillset.append(skill)    
        except:
            pass

    print len(skill_list)
    print len(skillset)
    print len(documents)
    resultSolution = pairwiseSimilarity(documents)
    print resultSolution

    l = skillset
    m = resultSolution.toarray()
    outputdict = dict(zip(l, map(lambda x: dict(zip(l,x)), m)))
    
    print outputdict
    with open('result.txt', 'w') as infile:
    	infile.write(json.dumps(outputdict))

    execfile("../floyd-warshall.py")
    completematrix=floydwarshall(outputdict, skillset)
    with open('complete.txt', 'w') as infile:
    	infile.write(json.dumps(completematrix))


