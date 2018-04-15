import os
import sys
import re
import glob
import string
import datetime
import langid as l

#Todo
	#Complete the model for Naive Bayes and Frequency Rank classifiers
	#Generate other models considering the factors to consider for the test
	#include the timer() to measure the time complexity of processing

def wordlist():
	#****************** START Model generator ********************************
	print ("\nLoading corpus files to memory and generating models ... ")
	path = 'corpus'
	mostfrequent = {} #the most frequent ngram in the corpus
	wordcount = {}
	grams = {}
	
	started = datetime.datetime.now()
	model =[]
	print ("{}\t{}\t{}\t{}\t{}\t{}\t    {}\t    {}\t    {}\t    {}".format('\nseq', 'term','freq','gram','lang','bytes','prob','InFreq','OvFreq','percent'))

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
			#transit = wordgrams(ngrams)
			#frequencyTable=frequencyTable+transit
			summary = l.summerize(model,l.wordgrams(ngrams),mostfrequent,wordcount,grams)

		except IOError:
			print ('Error: Can not open the file: ',lang)
			return	
	l.savetofile(summary, started)	

  #****************** END Model generator *******************************

def main():
	wordlist()
	#print (sys.stdout.encoding)
	
if __name__ == '__main__':
	main()