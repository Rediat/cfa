import os
import sys
import re
import copy
import glob
import string
import datetime
import langid as l

#Todo
	#Consider multilingual testing samples
	#include the timer() to measure the time complexity of processing

def sampling(selection=10):
		#****************** START Model generator ********************************
	print ("\nLoading testing files to memory and generating testing samples ... ")
	files = '*.txt'
	
	started = datetime.datetime.now()
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	base = dict(am=0,ge=0,gu=0,ti=0)
	counts = {}

	for i in range(1,selection+1):
		counts[i] = copy.deepcopy(base)

	for ct in range(1,11):
		path = 'corpus/testing/'+str(ct)+'/' ; path1 = 'samples/' ; samples = {}	
		duplicate = set() ; filename = str(ct)+'.txt' ; totals = 0
		for i in range(1,selection+1):
			counts[i] = copy.deepcopy(base)
		try:
			if os.path.isfile(os.path.join(path1, filename)): os.remove(os.path.join(path1, filename))
			s=open(os.path.join(path1,filename),'a+')

			print ('\n\n{}\nGenerating sample {}\n{}'.format('='*110,ct,'-'*110))			
			for infile in glob.glob(os.path.join(path, files)): #opens files from director
						
				cfilename = infile.split('/')[-1]
				lang = cfilename[:2]
				
				c=open(infile,'r')
				raw = c.read()
				c.close()
			
				#Word level parsing
				listed = l.regex([lang,raw])[1].strip()
				
				t=[0]; length = len(listed)

				for i in re.finditer(' ',listed):
					t.append(i.start())
				t.append(length)

				print('\n{} - Completed identifying phrase markers for {} language'.format(datetime.datetime.now(),language[lang]))
				
				test = [] ; r=len(t)-1

				for x,i in enumerate(t):
					print('\b'*40,end='')
					print('{} - {:0.2f}%'.format(datetime.datetime.now(),(x/r)*100),end='')
					for j in t:
						if(j>=t[x]):continue
						temp = listed[j:t[x]].strip()
						length = len(temp.split())
						if length>selection or temp in duplicate or len(temp)<2: continue
						temps = [lang,temp,sys.getsizeof(temp)]
						test.append(temps)
						duplicate.add(temp)
				
				samples[lang] = len(test)	
				print('\n{} - Created {:,} test phrases for {} language'.format(datetime.datetime.now(),samples[lang],language[lang]))

				r=len(test)-1

				for x,temp in enumerate(test):
					print('\b'*40,end='')
					print('{} - {:0.2f}%'.format(datetime.datetime.now(),(x/r)*100),end='')

					words = len(temp[1].split())
					counts[words][temp[0]]+=1

					#[lang,string,number of words,number of characters,bytes]
					s.write(str(temp[0])+","+str(temp[1])+","+str(words)+","+str(len(temp[1].strip()))+","+str(temp[2])+str('\r\n'))
			else:
				s.close()
		except IOError:
			print ('Error: Can not open the file: ','Corpus file {}.txt'.format(ct)) ; return		
			
		totals = sum(samples.values())
		print('\n\nsamples {}'.format(samples))
		
		print('\nWords \t Phrases \t Details')
		for i in range(1,selection+1):
			inlang = sum(counts[i].values())
			print('{:<3} \t {:,} \t\t {}'.format(i,inlang,counts[i]))

		print ('\n{:,} Test strings are successfuly created in {}{}.'.format(totals,path1,filename))
		print ('\nStarted:', started)
		ended = datetime.datetime.now()
		elapsed = ended - started
		print ('End    :', ended)
		print ('Elapsed:', elapsed)
		print ('\n')

def main():
	os.system('clear') # on linux 
	print ('\n\n{}'.format('='*100))
	print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - SAMPLER'.center(100,' '))
	print ('-'*100)  
	try:			
		choice = int(input('\nPress 1 to generate test phrases [0 to exit] :   '))

		if choice==0:
			return
		else:
			selection = int(input('\nEnter the maximum test phrese length in number of words :   '))
			if int(selection) == 0 or int(selection)>25:
				print ('\n\nPlease check your entry on max phrase length is >1')
			else:
					sampling(selection)
	except ValueError:
		print ('\n\nPlease check your entry on the process selection and try again')
		return

if __name__ == '__main__':
	main()