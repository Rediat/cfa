import os
import sys
import re
import glob
import string
import datetime
import langid as l

#Todo
	#Generate other models considering the factors to consider for the test

def clearCorpus():
	#****************** START Model generator ********************************
	os.system('clear')
	print ('\n\n{}'.format('='*100))
	print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - CORPUS CLEANER'.center(100,' '))
	print ('-'*100)	

	print ("\nLoading corpus files to memory ... ")
	path = 'corpus/rawSource/'
	
	started = datetime.datetime.now()
	
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

			cleantext=l.regex(rawtext)[1] #source file content set, i.e. vocabulary
			
			path1 = 'corpus/cleanSource/'
			if os.path.isfile(os.path.join(path1, filename)): os.remove(os.path.join(path1, filename))
			c=open(os.path.join(path1, filename),'a+')
			c.write(str(cleantext))
			c.close()

			print ('\nSuccessfuly cleande {} file '.format(filename))
			
		except IOError:
			print ('Error: Can not open the file: ',lang) ;	return	
	else:
	
		print ('\nStarted:', started)
		ended = datetime.datetime.now()
		elapsed = ended - started
		print ('End    :', ended)
		print ('Elapsed:', elapsed)

def main():
	clearCorpus()
	
if __name__ == '__main__':
	main()