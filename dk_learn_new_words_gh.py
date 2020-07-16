import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


fname = input("Enter file name: ")
fhand = open(fname, encoding="utf8")


word = list()
for line in fhand:
	line=line.split()
	word= word + line
#print(line)
print(word)