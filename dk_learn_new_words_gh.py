import string

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


#print(words)
	for word in words :
		print(word)
		url = "https://ordnet.dk/ddo/ordbog?query=%s" % (urllib.parse.quote(word)) # input('Enter URL- ')
		html = urllib.request.urlopen(url, context=ctx).read()
		
		
		soup = BeautifulSoup(html, 'html.parser')
		#print(soup)
		# # Retrieve all of the anchor tags
		tags = soup('div')
		
		for tag in tags:
			tag_class = tag.get('class', [])
			if "definitionBoxTop" in tag_class:
				# print(tag_class)
				children = tag.findChildren("span" , recursive=False)
				for child in children: 
					span_class = child.get('class', [])
					if "tekstmedium" in span_class:
						print(child.text)




