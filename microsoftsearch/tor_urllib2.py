import StringIO
import socket
import urllib2

import socks  # SocksiPy module
import stem.process

from stem.util import term

SOCKS_PORT = 7000

# Set socks proxy and wrap the urllib module

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

# Perform DNS resolution through the socket

def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

# Set socks proxy and wrap the urllib module

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

def print_bootstrap_lines(line):
     if "Bootstrapped " in line:
       print term.format(line, term.Color.BLUE)

print term.format("Starting Tor:\n", term.Attr.BOLD)

tor_process = stem.process.launch_tor_with_config(
     config = {
        'SocksPort': str(SOCKS_PORT),
        'ExitNodes': '{ru}',
     },
     init_msg_handler = print_bootstrap_lines,
)

def getUrl(url):

	def query(url):
	  """
	  Uses urllib to fetch a site using SocksiPy for Tor over the SOCKS_PORT.
	  """

	  try:
	      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
  	      hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                     'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                     'Accept-Encoding': 'none',
                     'Accept-Language': 'en-US,en;q=0.8',
                     'Connection': 'keep-alive'}
              opener.addheaders = hdr.items()
	      return opener.open(url).read()
	  except Exception as e:
	    return "Unable to reach " + url + " " + str(e)

	output = query(url)
	#tor_process.kill()  # stops tor
	return output

