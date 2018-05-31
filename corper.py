import os
import sys
import re
import copy
import glob
import string
import datetime
import langid as l

def corper():
		#****************** START Model generator ********************************
	print ("\nLoading testing files to memory and generating testing samples ... ")
	files = '*.txt'
	
	started = datetime.datetime.now()
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	
	path = 'corpus/cleanSource/' #; 
	# try:
	for infile in glob.glob(os.path.join(path, files)): #opens files from directory
				
		filename = infile.split('/')[-1]		
		lang = filename[:2]

		print ('\n\n{}\nGenerating Test and Trainin corpus for {}\n{}'.format('='*110,language[lang],'-'*110))
		
		c=open(infile,'r')
		raw = c.read()
		c.close()
	
		#Word level parsing
		listed = l.regex([lang,raw])[1].strip()
		
		length = len(listed)

		partition = int(length/10)

		marker = [x*partition for x in range(0,11)]

		for j, i in enumerate(marker):
			if j==i: continue					
			path1 = 'corpus/training/'+str(j)+'/' ; path2 = 'corpus/testing/'+str(j)+'/'
			# print (path1,path2,filename); return
			if os.path.isfile(os.path.join(path1, filename)): os.remove(os.path.join(path1, filename))
			if os.path.isfile(os.path.join(path2, filename)): os.remove(os.path.join(path2, filename))
			
			testing=listed[marker[j-1]:i]
			training = ' '.join([listed[:marker[j-1]],listed[i:]])

			tr=open(os.path.join(path1, filename),'a+')
			ts=open(os.path.join(path2, filename),'a+')

			ts.write(str(testing))
			tr.write(str(training))
			
			ts.close()
			tr.close()

			print('Corpus length: {}\t Training length: {}\t Testing Length: {}'.format(length,len(training),len(testing)))
			print('\n{} - Completed creating and training and testing corpus {} in file {}'.format(datetime.datetime.now(),j,filename))
			
			# print('training {} {}'.format(marker[j-1],len(listed[i:])))
			# print('{} training {}'.format(j,training))

			# print('testing {} {}'.format(j-1,i))
			# print('{} testing {}'.format(j,testing))				

	else:
		print ('\nStarted:', started)
		ended = datetime.datetime.now()
		elapsed = ended - started
		print ('End    :', ended)
		print ('Elapsed:', elapsed)
		print ('\n')

	# except IOError:
	# 	print ('Error: Can not open the files') ; return		

def main():
	os.system('clear') # on linux 
	choice =1
	while choice!=0:
		print ('\n\n{}'.format('='*100))
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - CORPUS CREATOR'.center(100,' '))
		print ('-'*100) 
			
		choice = int(input('\nPress 1 to generate test phrases [0 to exit] :   '))

		if choice==0: break
		elif choice<0 or choice>1:
			print ('\n\nPlease check your entry on the process selection and try again')
		else:
			corper()

if __name__ == '__main__':
	main()