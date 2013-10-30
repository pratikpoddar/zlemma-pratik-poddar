from wikipedia_extractor import Wikipedia, Wiki2Plain
import urllib
from tfidf import pairwiseSimilarity

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
    
if __name__ == "__main__":
    execfile("../skill_list.py")
    skill_list = map(lambda x: x.replace("-", " "), skill_list)	
    for skill in skill_list:
        save_page(skill)
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
    
    execfile("../floyd-warshall.py")
    completematrix=floydwarshall(outputdict, skillset)

