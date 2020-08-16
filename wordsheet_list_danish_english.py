
import string

# .. Text Tranlator ..
import googletrans
from googletrans import Translator
translator = Translator()

# Color to the promt 
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
# import openpyxl module 
# import openpyxl 
import xlrd


# 			READ FORMER EXCEL 

# ----------------- P A T H -----------------------------------
PATH_XLS_FILE='C:\\Users\\Ana Maria\\Documents\\DS\\APP_DK_ord\\'
# ----------------- P A T H -----------------------------------



# --------------D I C T I O N A R Y ---------------------------------
dict_word_type={}
# --------------D I C T I O N A R Y ---------------------------------


from xlrd import open_workbook

col_index=0

book = open_workbook('DK_WORDS_0.xlsx')
sheet = book.sheet_by_index(0)

# read first row - Header 
keys = sheet.row_values(0)
print(keys)
#  read each rows 
for i in range(1, sheet.nrows):
	row = sheet.row_values(i)
#  K E Y 
	k_word = row[0]

#   V A L U E S 
	k_phonema = row[1]
	k_type = row[2]
	k_meaning = row[3]
	k_sound = row[4]
	k_sentence = row[5]
	k_translation = row[6]

#  ..........  D I C T I O N A R T    T U P L E    ..............
	dict_word_type[k_word]= (k_phonema,k_type, k_meaning, k_sound, k_sentence,k_translation) # key-> tuple

#print(dict_word_type)
#print(dict_word_type["elsker"])
	#... = row[1])
	#print(row[2])
	#print(row[3])


# for value in values:
#     dict_list.append(dict(zip(keys, value)))

# print (dict_list)

#===================

# Ignore SSL certificate errors - Type of words 
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


######## INPUT SENTECE FILE ######
fname = input("Enter file name: ")
fhand = open(fname, encoding="utf8")

# Get rid out of punctuation
SYMBOLS = '{}()![].,:;+-*/&|<>=~$1234567890?'

# List list() or var=[ ]

# DEFINITION OF WORD LIST
words = list()

# DEFINITION OF SENTENCE LIST
sentences=" "

# REMOVE SYMBOLS 
for line in fhand:
	#sentences.append(line) 
	
	sentences= sentences + line
	print( Fore.BLUE + str(sentences)) 
	for s in SYMBOLS:
		line = line.replace(s," ")
	#print(Fore.MAGENTA +  line)
	line1=line.split()
	
	words= words + line1
	translation=translator.translate(sentences, src='da', dest='en')
	g_translation= str(translation.text)
	print(Fore.GREEN + g_translation)
	 
#----------------- csv mode --------------------------
#-with open("DK_WORDS.xlsx", 'w') as file:
#	file.write("Word" + "," + "Type" + "," +  "Sound" )
#s	file.write("\n")
#----------------- csv mode --------------------------

# PROPERTIES FROM WORD: Meaning, Type, Phoneme, Sentence, Sound

	for word in words :
		print(Fore.YELLOW + "Searching: "+ word)

		#  STRINGS FOR DICTIONARY
		meaning= ""
		type_word= ""
		phonema= ""
		mp3= ""
		not_found= ""


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
				# Target the type of word 
				if "definitionBoxTop" in div_class:
					# print(div_class)
					children = div.findChildren("span" , recursive=False)
					for child in children: 
						span_class = child.get('class', [])
						if "tekstmedium" in span_class:
#............................ T Y P E   O F   W O R D ................................... 

							type_word=child.text
							print(type_word)

						if "match" in span_class:
							root_word=child.text
							for s in SYMBOLS:
								root_word = root_word.replace(s," ")

							print(Fore.CYAN  + root_word )

# PHONEME AND SOUND	
			span = soup.body.find('span', attrs={'class': 'lydskrift'})
#............................ P H O N E M A ................................... 
			phonema=span.text
			print(Fore.GREEN +  phonema)


			for href in span.find_all('a', recursive=True):
#............................ S O U N D   M P 3 ................................... 
				mp3=href.get('href', "NotFound")	
				print( Fore.MAGENTA + str(mp3) )


# English meaning
			url = "https://en.bab.la/dictionary/danish-english/%s" % (urllib.parse.quote(root_word)) 
			html = urllib.request.urlopen(url, context=ctx).read()
			soup = BeautifulSoup(html, 'html.parser')
			span = soup.body.find('ul', attrs={'class': 'sense-group-results'})
#			print(span)
#............................ M E A N I N  G  ................................... 
			meaning=span.text 

			print(Fore.RED + meaning + "\n ")

#............................ T R A N S L A T I O N  ................................... 

			
# 							NEW DICTIONARY 

			dict_word_type[word]= (phonema,type_word, meaning, mp3, str(sentences), g_translation) # key-> tuple


		except:
			print("not found " )
			meaning="not found "
			dict_word_type[word]= ("", "", meaning, "", str(sentences), g_translation) # key-> tuple
			

#CSV MODE
#		file.write(word  + type_word  + mp3 +  "," + str(line)  )
#		file.write("\n")


#----------------- E X C E L --------------------------
	current_line=0

	PATH_XLS_FILE='C:\\Users\\Ana Maria\\Documents\\DS\\APP_DK_ord\\'
	workbook = xlsxwriter.Workbook( PATH_XLS_FILE  + "DK_WORDS_0.xlsx" )
	
	# Call a Workbook() function of openpyxl  
	# to create a new blank Workbook object 
	# workbook = openpyxl.Workbook() 
  	# Get workbook active sheet   
	# from the active attribute.  
	# sheet = workbook.active 
  	# writing to the specified cell 
	# sheet.column_dimensions['E'].width = 50
	# workbook.save(  PATH_XLS_FILE  + "DK_WORDS.xlsx") 
	#worksheet1.set_column(20, 20, 20,50)
		# Cell color for header names - Tipo B Tipo C Tipo D  Period  Intensity
	cell_format = workbook.add_format({'bold': True, 'font_color': 'white'})
	cell_format.set_bg_color('#004C99')
	cell_format.set_text_wrap()
	cell_format.set_align('center')
	cell_format.set_align('top')
	cell_format.set_border(1)
# Creating Worksheets
	current_sheet = workbook.add_worksheet("ALL_TYPES")
#	current_sheet = workbook.add_worksheet("Sounds")
#	current_sheet = workbook.add_worksheet("Vocabulary")
#	current_sheet = workbook.add_worksheet("Conjunction")

	current_sheet.write(0, 0 , "Word", cell_format)
	current_sheet.write(0, 1 , "Phonema", cell_format)
	current_sheet.write(0, 2 , "Type", cell_format)
	current_sheet.write(0, 3 , "Meaning", cell_format)
	current_sheet.write(0, 4 , "Sound", cell_format)
	current_sheet.write(0, 5 , "Sentence", cell_format)
	current_sheet.write(0, 6 , "Translation", cell_format)
#----------------- excel mode --------------------------

	for all_word in dict_word_type:
		(all_phonema, all_type, all_meaning, all_sound, all_sentences, all_translation) = dict_word_type[all_word]
		current_sheet.set_column('A:A', 20)
		current_sheet.set_column('C:C', 20)
		current_sheet.set_column('D:D', 25)
		current_sheet.set_column('F:F', 80) 
		current_sheet.set_column('G:G', 80)
		current_line= current_line + 1
		current_sheet.write(current_line, 0 , all_word )
		current_sheet.write(current_line, 1 , all_phonema )
		current_sheet.write(current_line, 2 ,all_type)
		current_sheet.write(current_line, 3 , all_meaning )
		current_sheet.write(current_line, 4 , all_sound)
		current_sheet.write(current_line, 5 , all_sentences )
		current_sheet.write(current_line, 6 , all_translation)


workbook.close()
#	file.write(type_word)
#	file.write("\n")


import os
os.system("start EXCEL.EXE "  + "\"" +PATH_XLS_FILE + "DK_WORDS_0.xlsx" + "\"")





