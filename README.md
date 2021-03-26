# Learning Danish Words
## Introduction

This tool creates, registers and storages the words and its properties from an input Danish Language text.  

From a sentence given as a text, the tool take each word and look after their meaning and the word properties in the Danish dictionary (Ordnet).
After that the result is print in an Excel file.
Its properties are:

- Meaning in english.
- Grammatical property (adjective, verbs, noun, etc).
- Sound (mp3).
- Phoneme.
- Sentence that contains the word.
- English sentence translation.

## Data Source

- Danish Dictionary
https://ordnet.dk

- English-Danish Dictionary
https://en.bab.la/dictionary/danish-english

## App to install
In order this tool works it needs some installations

googletrans - for translate sentence
xlsxwriter - to work with excel files
BeautifulSoup - to extract data from webpages
sys - for color in the command prompt


### Input Files:

- Excel Sheet with specified columns, word properties(meaning, phoneme, grammar type, etc)
- ASSCCI Text, where you add the sentence (input).

### Output File:
- Excel Sheet with the words and properties from the sentence.

![sheetJPG](https://user-images.githubusercontent.com/52880203/90572036-58986780-e1b3-11ea-8695-4f7faa48e8c2.JPG)

### Steps

 - Modify the Excel sheet file path by yours in **line29** .


PATH_XLS_FILE='C:\\Users\\Ana Maria\\Documents\\DS\\APP_DK_ord\\'


- Modify the name of your Excel sheet as the one you have in **line 43**

book = open_workbook('DK_WORDS_0.xlsx')

- Run the script in an cmd, it will ask you the name of your txt file, where it is the sentence you want to get the words. Write down the file name.
