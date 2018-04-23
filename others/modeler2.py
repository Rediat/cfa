import os
import sys
import re
import glob
import string
import datetime
import langid2 as l

#Todo
	#Complete the model for Naive Bayes and Frequency Rank classifiers
	#Generate other models considering the factors to consider for the test
	#include the timer() to measure the time complexity of processing

def wordlist():
	#****************** START Model generator ********************************
	os.system('clear')
	print ('\n{} - Loading corpus files to memory and generating models ...'.format(datetime.datetime.now()))
	path = 'corpus'
	mostfrequent = {} #the most frequent ngram in the corpus
	wordcount = {} ; vocabulary = {}
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	started = datetime.datetime.now()
	model =[]
	# print ("{}\t{}\t{}\t{}\t{}\t{}\t    {}\t    {}\t    {}\t    {}".format('\nseq', 'term','freq','gram','lang','bytes','prob','InFreq','OvFreq','percent'))

	for infile in glob.glob(os.path.join(path, '*.txt')): #opens files from director
		try:
			#Extract the file name			
			filename = infile.split('/')[-1]
			lang = filename[:2]

			#open and read file from corpus
			f=open(infile,'r')#, encoding = 'utf8' )
			raw = f.read()
			rawtext = [lang,raw]
			f.close()

			#Ngram level parsing
			ngrams = l.ngram(l.regex(rawtext))
			
			print('{} - Completed removing punctuation marks and numbers for {} language'.format(datetime.datetime.now(),language[lang]))
			summary = l.summerize(model,l.wordgrams(ngrams),mostfrequent,wordcount,vocabulary)
			print('{} - Completed building sorted frequency distribution for {} language'.format(datetime.datetime.now(),language[lang]))
			print('-'*110)
			
		except IOError:
			print ('Error: Can not open the file: ',lang)
			return
	print('{} - Saving the model for all languages to model.txt'.format(datetime.datetime.now()))	
	l.savetofile(summary, started)	

  #****************** END Model generator *******************************

def main():
	wordlist()
	#print (sys.stdout.encoding)
	
if __name__ == '__main__':
	main()