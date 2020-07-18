import string
import sys
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


fname = input("Enter file name: ")
fhand = open(fname, encoding="utf8")


SYMBOLS = '{}()[].,:;+-*/&|<>=~$1234567890?'
words = list()
for line in fhand:
	for s in SYMBOLS:
		line = line.replace(s," ")
	print(line)
	line=line.split()
	
	words= words + line

# TYPE OF WORD
	for word in words :
		print(Fore.YELLOW + word)
		try:
			url = "https://ordnet.dk/ddo/ordbog?query=%s" % (urllib.parse.quote(word)) # input('Enter URL- ')
			html = urllib.request.urlopen(url, context=ctx).read()
		
			soup = BeautifulSoup(html, 'html.parser')
			#print(soup)
			# # Retrieve all of the anchor divs
			divs = soup('div')
			for div in divs:
				div_class = div.get('class', [])
				if "definitionBoxTop" in div_class:
					# print(div_class)
					children = div.findChildren("span" , recursive=False)
					for child in children: 
						span_class = child.get('class', [])
						if "tekstmedium" in span_class:
							type_word=child.text
							print(Fore.CYAN  + type_word)
# SOUND	
			span = soup.body.find('span', attrs={'class': 'lydskrift'})
			print(span.text)
			for href in span.find_all('a', recursive=True):
				print( Fore.GREEN + str(href.get('href', "NotFound")))

		except:
			print(Fore.RED + "not found " )






