import string

import sys
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)
# socket webpage retrieval
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
# xlwt is a library to export and work in excel sheet
import xlsxwriter

# Ignore SSL certificate errors - Type of words 
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE




fname = input("Enter file name: ")
fhand = open(fname, encoding="utf8")

# Not to take in account punctuation
SYMBOLS = '{}()[].,:;+-*/&|<>=~$1234567890?'
words = list()
for line in fhand:
	for s in SYMBOLS:
		line = line.replace(s," ")
	print(Fore.MAGENTA +  line)
	line1=line.split()
	
	words= words + line1
#----------------- csv mode --------------------------
#-with open("DK_WORDS.xlsx", 'w') as file:
#	file.write("Word" + "," + "Type" + "," +  "Sound" )
#s	file.write("\n")
#----------------- csv mode --------------------------
#----------------- excel mode --------------------------
	current_line=0

	PATH_XLS_FILE='C:\\Users\\Ana Maria\\Documents\\DS\\APP_DK_ord\\'
	workbook = xlsxwriter.Workbook( PATH_XLS_FILE  + "DK_WORDS.xlsx" )
		# Cell color for header names - Tipo B Tipo C Tipo D  Period  Intensity
	cell_format = workbook.add_format({'bold': True, 'font_color': 'white'})
	cell_format.set_bg_color('#004C99')
	cell_format.set_text_wrap()
	cell_format.set_align('center')
	cell_format.set_align('top')
	cell_format.set_border(1)

	current_sheet = workbook.add_worksheet("ALL_TYPES")
#	current_sheet = workbook.add_worksheet("Pronoun")
#	current_sheet = workbook.add_worksheet("Adverb")
#	current_sheet = workbook.add_worksheet("Conjunction")

	current_sheet.write(0, 0 , "Word", cell_format)
	current_sheet.write(0, 1 , "Type", cell_format)
	current_sheet.write(0, 3 , "Sound", cell_format)
	current_sheet.write(0, 4 , "Example", cell_format)
	current_sheet.write(0, 2 , "Meaning", cell_format)
#----------------- excel mode --------------------------

# TYPE OF WORD

	for word in words :
		print(Fore.YELLOW + "Searching: "+ word)
		meaning= ""
		type_word= ""
		mp3= ""
		try:
			#socket
			url = "https://ordnet.dk/ddo/ordbog?query=%s" % (urllib.parse.quote(word)) # input('Enter URL- ')
			html = urllib.request.urlopen(url, context=ctx).read()
			#retrieve all of the anchor tags
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

						if "match" in span_class:
							root_word=child.text
							for s in SYMBOLS:
								root_word = root_word.replace(s," ")

							print(Fore.BLUE  + root_word )


# SOUND	
			span = soup.body.find('span', attrs={'class': 'lydskrift'})
			print(span.text)
			for href in span.find_all('a', recursive=True):

				mp3=href.get('href', "NotFound")	
				print( Fore.GREEN + str(mp3) )


# English meaning
			url = "https://en.bab.la/dictionary/danish-english/%s" % (urllib.parse.quote(root_word)) 
			html = urllib.request.urlopen(url, context=ctx).read()
			soup = BeautifulSoup(html, 'html.parser')
			span = soup.body.find('ul', attrs={'class': 'sense-group-results'})
#			print(span)
			meaning=span.text 
			print(Fore.RED + meaning + "\n ")
		except:
			print("not found " )


#CSV MODE
#		file.write(word  + type_word  + mp3 +  "," + str(line)  )
#		file.write("\n")

		current_line= current_line + 1

		current_sheet.write(current_line, 0 , word )
		current_sheet.write(current_line, 1 , type_word)
		current_sheet.write(current_line, 3 , mp3)
		current_sheet.write(current_line, 4 , str(line))
		current_sheet.write(current_line, 2 , meaning )


workbook.close()
#	file.write(type_word)
#	file.write("\n")


import os
os.system("start EXCEL.EXE "  + "\"" +PATH_XLS_FILE + "DK_WORDS.xlsx" + "\"")


