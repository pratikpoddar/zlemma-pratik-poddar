import gevent
import urllib2
from gevent.pool import Pool
from BeautifulSoup import BeautifulSoup
import FileUtil

import grequests
proxy_servers = FileUtil.readJson("/var/tmp/proxy_servers.json")


class Scraper(object):
    def __init__(self, proxy):
        self._open = self._get_opener(proxy)
        self.proxy = proxy

    def _get_opener(self, proxy):
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        return opener.open

    def get_soup(self, url):
        try:
            print "Trying : " + self.proxy + ", " + str(url)
            request = grequests.get(url)
            responses = grequests.map([request])
            response = responses[0].text
            soup = BeautifulSoup(response)
            return soup
        except:
            return "Failed"


class MultiThreadedScraper(object):

    def __init__(self, proxies=proxy_servers):
        self.proxy_servers = proxies
        self.pool = Pool(len(proxies))
	self.reset_proxies("http://www.google.com")

    def reset_proxies(self, url):
        self.proxy_servers = FileUtil.readJson("/var/tmp/proxy_servers.json")
        global proxy_servers
        proxy_servers = self.proxy_servers

        test_jobs = []
        for i in xrange(0, len(self.proxy_servers)):
            scraper = Scraper(self.proxy_servers[i])
            test_jobs.append(self.pool.spawn(scraper.get_soup, url))
        gevent.joinall(test_jobs)
        test_outputs = [job.value for job in test_jobs]

        good_servers = []
        for i in xrange(0, len(test_outputs)):
            value = test_outputs[i]
            if value != "Failed":
                good_servers.append(self.proxy_servers[i])

        self.proxy_servers = good_servers
        self.scrapers = [Scraper(server) for server in self.proxy_servers]
        proxy_servers = good_servers

    def scrape(self, urls, retry_count=0):
        if len(self.scrapers) == 0:
            print "No Scraper Found"
            return {}
        count = 0
        jobs = []
        proxy_servers = []
        for url in urls:
            scraper = self.scrapers[count % len(self.scrapers)]
            jobs.append(gevent.spawn(scraper.get_soup, url))
            proxy_servers.append(scraper.proxy)
            count = count + 1
        gevent.joinall(jobs)
        outputs = [job.value for job in jobs]
        output_map = {}
        failed_urls = []
        failed_server = []
        for i in xrange(0, len(outputs)):
            value = outputs[i]
            if value != "Failed":
                print "Fetched Url : " + str(urls[i])
                output_map[urls[i]] = value
            else:
                print "Failed Url : " + str(urls[i])
                failed_server.append(proxy_servers[i])
                failed_urls.append(urls[i])

        good_servers = [server for server in self.proxy_servers
                        if server not in failed_server]

        if len(good_servers) > 0 and retry_count < 3:
            self.scrapers = [Scraper(server) for server in good_servers]
            final_outputs = self.scrape(failed_urls, retry_count + 1)
            for final_output in final_outputs:
                output_map[final_output] = final_outputs[final_output]

        else:
            for failed_url in failed_urls:
                if failed_url not in output_map:
                    output_map[failed_url] = failed_url
        return output_map

if __name__ == "__main__":
    scraper = MultiThreadedScraper(proxy_servers)
    urls = ["http://en.wikipedia.org/w/api.php?format=json&action=query&titles=stanford&prop=categories&redirects",
            "https://google.com",
            "http://www.google.com/search?q=MIT"]
    outputmap = scraper.scrape(urls)
