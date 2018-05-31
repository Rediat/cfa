import os ; import sys ; import re ; import glob
import string ; import datetime ; import langid as l

def modeler(started, mod,wordbased=0,location=0,infinity=0):
	#****************** START Model generator ********************************
	print ('\n{}'.format('='*110))
	print ('\n{} - Loading corpus files to memory and generating models ...'.format(datetime.datetime.now()))

	files = '*.txt'
	mostfrequent = {} #the most frequent ngram in the corpus
	wordcount = {} ; vocabulary = {}
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	maxg = 5

	started = datetime.datetime.now()
	myfile=mod+'.txt'
	for ct in range(1,11):
		path = 'corpus/training/'+str(ct)+'/' ; model =[]
		print ('\n{}\nProcessing corpus {}\n{}'.format('='*110,ct,'-'*110))	
		for infile in glob.glob(os.path.join(path, files)): #opens files from director
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

				'''\nSelect Model type number below: \n\n   
				1. The Model is based on Fixed Length N-grams without location features - Baseline [bl]. \n
				2. The Model is based on source text - Byteorder N-grams [by]. \n
				3. The Model is based on Fixed Length N-grams with location features [fl]. \n
				4. The Model is based on Infiniti-grams without location features [in]. \n   
				5. The Model is based on Infiniti-grams with location features [il]. \n
				6. The Model is based on Word Frequency without location features [wr]. \n
				7. Exit.:   '))
				'''
				if mod=='bl': #to generate ngrams from source text wordbased baseline
					temp = l.regex(rawtext)[1].split()
					wordlist = []
					for i in temp:
						wordlist.extend(l.ngram([lang,i])[1])
					ngrams=[lang,wordlist,mod]
				
				elif mod=='by': #to generate ngrams from source text fixed byteorder
					ngrams = l.ngram(l.regex(rawtext))
					ngrams.append(mod)
					
				elif mod=='fl': #to generate ngrams model (inifinigram) from words taken from source files
					temp = l.regex(rawtext)[1].split()
					wordlist = []
					for i in temp:
						wordlist.extend(l.ngram([lang,i],0,location,infinity)[1])
					ngrams=[lang,wordlist,mod]

				elif mod=='il' or mod=='in': #to generate ngrams model (inifinigram) from words taken from source files
					temp = l.regex(rawtext)[1].split()
					wordlist = []
					for i in temp:
						maxg = len(i) if maxg <	len(i) else maxg #Indicate the model type [T-top n,B-byteorder,I-infinitigram,L-infinitigram with location feature, W-word frequency model]
						if location==0:
							wordlist.extend(l.ngram([lang,i],0,location,infinity)[1])
						else:
							wordlist.extend(l.ngram([lang,i],0,location,infinity)[1])
					ngrams=[lang,wordlist,mod]
					
				elif mod=='wr': #to generate word frequency model from source files
					temp = l.regex(rawtext)[1].split()
					ngrams = [lang,temp,mod]
							
				print('\t{} - Completed removing punctuation marks and numbers for {} language'.format(datetime.datetime.now(),language[lang]))
				summary = l.summerize(model,l.wordgrams(ngrams),mostfrequent,wordcount,vocabulary)

				print('\t{} - Completed building sorted frequency distribution for {} language'.format(datetime.datetime.now(),language[lang]))
				print('{}{}'.format('\t','-'*100))
				
			except IOError:
				print ('Error: Can not open the file: ',lang)
				return
		print('{} - Saving the model for all languages to models/{}/{}'.format(datetime.datetime.now(),ct,myfile))
			
		l.savetofile(summary,started,mod,maxg,ct)

  #****************** END Model generator *******************************

def main():
	os.system('clear') # on linux 
	choice=1 ; modeltype = {1:'wr', 2:'bl', 3:'by', 4:'fl', 5:'in', 6:'il'}
	while choice!=0:
		location=0 ; infinity=0; mod='' ; wordbased=0
		print ('\n\n{}'.format('='*110)) ; started=datetime.datetime.now()
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - MODELLER'.center(110,' '))
		print ('-'*110)  
		try:			
			choice = int(input('\nPress 1 to generate models [0 to exit] :   '))
			if choice==0: return
			else:
				ind = int(input('\nSelect Model type number below: \n\n   1. The Model is based on Word Frequency without location features [wr] \n   2. The Model is based on Fixed Length N-grams without location features - Baseline [bl]. \n   3. The Model is based on source text - Byteorder N-grams [by]. \n   4. The Model is based on Fixed Length N-grams with location features [fl]. \n   5. The Model is based on Infiniti-grams without location features [in]. \n   6. The Model is based on Infiniti-grams with location features [il]. \n   7. Exit.:   '))
				if ind==7: choice=0 ; return

				'''\nSelect Model type number below: \n\n   
				1. The Model is based on Word Frequency without location features [wr]. \n
				2. The Model is based on Fixed Length N-grams without location features - Baseline [bl]. \n
				3. The Model is based on source text - Byteorder N-grams [by]. \n
				4. The Model is based on Fixed Length N-grams with location features [fl]. \n
				5. The Model is based on Infiniti-grams without location features [in]. \n   
				6. The Model is based on Infiniti-grams with location features [il]. \n
				7. Exit.:   '))
				'''
				if modeltype[ind]=='bl':
					wordbased=1 ; location=0 ; infinity=0 ; mod='bl'
				elif modeltype[ind]=='fl': 
					wordbased=1 ; location=1 ; infinity=0 ; mod='fl'
				elif modeltype[ind]=='in': 
					wordbased=1 ; location=0 ; infinity=1 ; mod='in'
				elif modeltype[ind]=='il': 
					wordbased=1 ; location=1 ; infinity=1 ; mod='il'
				elif modeltype[ind]=='wr': 
					wordbased=0 ; location=0 ; infinity=0 ; mod='wr'
				else: 
					wordbased=0 ; location=0 ; mod=modeltype[ind]

				if ind < 0 or ind>7:
					print ('\n\nPlease check your entry on model selection')
				else:
					# ct = corpustype[ctype]
					modeler(started,mod,wordbased,location,infinity)
			
			print ('\nStarted:', started)
			ended = datetime.datetime.now()
			elapsed = ended - started
			print ('End    :', ended)
			print ('Elapsed:', elapsed)

		except ValueError:
			print ('\n\nPlease check your entry on model selection [either 0 or 1]')
	
if __name__ == '__main__':
	main()