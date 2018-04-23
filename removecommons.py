import os
import sys
import re
import glob
import string
import datetime
import langid as l

#Todo
	#Generate other models considering the factors to consider for the test

def clearCommons():
	#****************** START Model generator ********************************
	os.system('clear')
	print ("\n Loading corpus files to memory and generating models ... ")
	path = 'corpus/300'
	
	alllist =[] ; vocabulary = set()
	started = datetime.datetime.now()
	content = {}
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	
	commons =set()
	
	for infile in glob.glob(os.path.join(path, '*.txt')): #opens files from directory
		try:
			#Extract the file name			
			filename = infile.split('/')[-1]
			lang = filename[:2]

			#open and read file from corpus
			f=open(infile,'r', encoding = 'utf8' )
			rawtext = [lang,f.read()]
			f.close()

			print ('-'*100) 
			print ('\nOpening relevant files ...  \t\t\t\t\t\t{}'.format(l.timer(started)))

			content[lang]=set(l.regex(rawtext)[1].split())
			
			listed = l.regex(rawtext)[1].split()
			alllist.append(listed)

			for i in content: #update the set vocabulary with the union of itself and a new list.
				vocabulary.update(content[i])

			print('{} - Completed building relevant dictionaries for {} language'.format(datetime.datetime.now(),language[lang]))
		
		except IOError:
			print ('Error: Can not open the file: ',lang)
			return	
	
	r = len(vocabulary) ; w = 0
	for i in content:
		w+= len(content[i])

	print ('-'*100)
	print('{} - Matching {:,} vocabulary items to {:,} ngrams in all language'.format(datetime.datetime.now(),r,w))
	
	for i in content:	
		for j in content:
			if i==j:continue
			commons.update(content[i].intersection(content[j]))

	path1 = 'corpus/clearedcommons/300'
	for infile in glob.glob(os.path.join(path, '*.txt')):
		filename = infile.split('/')[-1] ; lang = filename[:2]
		if os.path.isfile(os.path.join(path1, filename)): os.remove(os.path.join(path1, filename))
		
		f=open(infile,'r')
		rawtext = l.regex([lang,f.read()])[1]
		f.close()
		
		cleared = ' '.join(filter(lambda x: x not in commons,  rawtext.split()))
		c=open(os.path.join(path1, filename),'a+')
		c.write(str(cleared))
		c.close()

	print ('\nA total of {} common terms in commons.txt file are removed for the corpus '.format(len(commons)))

	if os.path.isfile('commons.txt'): os.remove('commons.txt')
	s=open('commons.txt','a+')
	s.write(str(commons))
	s.close()
	
	print ('\nStarted:', started)
	ended = datetime.datetime.now()
	elapsed = ended - started
	print ('End    :', ended)
	print ('Elapsed:', elapsed)

def main():
	clearCommons()
	#print (sys.stdout.encoding)
	
if __name__ == '__main__':
	main()