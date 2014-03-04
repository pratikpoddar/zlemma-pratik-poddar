import urllib
import unidecode
from utils.scraper.proxy import MultiThreadedScraper
import time


scraper = MultiThreadedScraper()


def get_titles(titles, callback=None):
    encoded_titles = []
    for title in titles:
        urlencoded_title = unidecode.unidecode(title)
        urlencoded_title = urlencoded_title.encode('ascii')
        urlencoded_title = urllib.quote(urlencoded_title)
        urlencoded_title = "http://www.google.com/search?q=" + urlencoded_title
        encoded_titles.append(urlencoded_title)

    scraper.reset_proxies(encoded_titles[0])
    chunk = []
    chunk_titles = []
    output = []
    for count in xrange(0, len(encoded_titles)):
        if count % 100 == 99:
            output += process_chunk(chunk, chunk_titles, callback)
            chunk = [encoded_titles[count]]
            chunk_titles = [titles[count]]
        else:
            chunk.append(encoded_titles[count])
            chunk_titles.append(titles[count])
    output += process_chunk(chunk, chunk_titles, callback)
    return output

def process_chunk(chunk, chunk_titles, callback, retry_count=0):
    output = []
    result_map = scraper.scrape(chunk, chunk_titles)
    results = [result_map.get(url, None) for url in chunk]
    is_valid = False
    for result in results:
        if result != "Failed":
            is_valid = True
            break

    if not is_valid:
        print "Timing Out for 1800 sec"
        time.sleep(2)
    if not is_valid:
        time.sleep(1800)
        process_chunk(chunk, chunk_titles, callback, retry_count + 1)

    count = 0

    for i in xrange(0, len(results)):
        result = results[i]
        wiki_link = extract_wiki_link(result)
        if wiki_link:
            count = conut + 1
            print wiki_link
            output.append(wiki_link)
        else:
            output.append(None)
    if callback:
        callback(output, chunk_titles)
    print "Number of wiki links : " + str(count)

    if count == 0:
        time.sleep(1800)

    time.sleep(100)
    return output


def extract_wiki_link(soup):
    try:
        for cite in soup.findAll('cite'):
            scraped_url = unidecode.unidecode(cite.text)
            if "wikipedia" in scraped_url and "List_of" not in scraped_url:
                return scraped_url.split("/")[-1]
    except:
        return None
    return None

if __name__ == "__main__":
    titles = [
        "MIT",
        "IIT-DELhi",
        "IITB",
        "Microsoft"
    ]
    print get_titles(titles)
