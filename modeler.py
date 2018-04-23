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
	#Include the timer() to measure the time complexity of processing

def modeler(ind,charlength):
	#****************** START Model generator ********************************
	print ('\n{} - Loading corpus files to memory and generating models ...'.format(datetime.datetime.now()))
	path = 'corpus/clearedcommons/300'
	# path = 'corpus'
	mostfrequent = {} #the most frequent ngram in the corpus
	wordcount = {} ; vocabulary = {}
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')

	started = datetime.datetime.now()
	model =[]

	for infile in glob.glob(os.path.join(path, '*.txt')): #opens files from director
		try:
			#Extract the file name			
			filename = infile.split('/')[-1]
			lang = filename[:2]

			#Open and read file from corpus
			f=open(infile,'r')#, encoding = 'utf8' )
			raw = f.read()
			rawtext = [lang,raw]
			f.close()

			#Word/Ngram level parsing
			ngrams=[]
			if ind==0:
				ngrams = l.ngram(l.regex(rawtext))
			
			elif ind==1:
				temp = l.regex(rawtext)[1].split()
				# ngrams = [lang,temp] #uncomment this and comment the below to revert to word model
				for i in temp:
					if len(i)>charlength:continue
					ngrams[lang].extend(l.ngram([lang,i])[1])
			
			else:
				temp = l.regex(rawtext)[1].split()
				ngrams = [lang,temp] #uncomment this and comment the below to revert to word model
			
			
			print('\t{} - Completed removing punctuation marks and numbers for {} language'.format(datetime.datetime.now(),language[lang]))
			summary = l.summerize(model,l.wordgrams(ngrams),mostfrequent,wordcount,vocabulary)
			print('\t{} - Completed building sorted frequency distribution for {} language'.format(datetime.datetime.now(),language[lang]))
			print('{}{}'.format('\t','-'*100))
			
		except IOError:
			print ('Error: Can not open the file: ',lang)
			return
	print('{} - Saving the model for all languages to model.txt'.format(datetime.datetime.now()))
		
	l.savetofile(summary, started,ind)	

  #****************** END Model generator *******************************

def main():
	os.system('clear') # on linux 
	print ('\n\n{}'.format('='*100))
	print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION'.center(100,' '))
	print ('-'*100)  
	try:			
		choice = int(input('\nPress 1 to generate models [0 to exit] :   '))

		if choice==0:
			return
		else:
			ind = int(input('\nPlease choose 0 for ngram or 1 for infinitigram or 2 for word frequency model :   '))
			charlength = 25
			if ind==1:				
				charlength = int(input('\nPlease chose between 2 and 5 for limited word character lenght [25 to consider all]:   '))
			if int(ind) < 0 or int(ind)>2 or charlength<2:
				print ('\n\nPlease check your entry on model selection [either 0 or 1]')
			else:
				modeler(ind,charlength)
	except ValueError:
		print ('\n\nPlease check your entry on model selection [either 0 or 1]')
		return
	#print (sys.stdout.encoding)
	
if __name__ == '__main__':
	main()