import os
import sys
import re
import glob
import string
import datetime
import copy
import decimal
import langidb as l

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
	#Consider multilingual testing samples
	#[Build classifier for Naive Bayes and Frequency Rank]
	#Create a file that execues modeler sampler and classifier one after the other execute.py
	#modularize classifier.py in to functions - move functions in to another file
	#measure performace based on number of words in sample query

def classification(phraselength,percent=1,lowfreq=0):
	#phraselength=5
	#*************************** START Reading Files ************************************

	started = datetime.datetime.now()
	maxngram = 5
	f=open('model.txt','r') #, encoding = 'utf8' )
	#m=open('metrix.txt','r', encoding = 'utf8' )
	s=open('sample.txt','r') #, encoding = 'utf8' )

	print ('-'*100) 
	print ('\nOpening relevant files ...  \t\t\t\t\t\t{}'.format(l.timer(started)))
	mytime = datetime.datetime.now()
	
	model = f.readlines()
	#matrix = m.read()
	print ('Reading language models ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	sample = s.readlines()
	f.close()
	s.close()
	#m.close()
	#*************************** END Reading Files ***************************************
	print ('Reading test strings ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	sampled= l.readsample(sample,phraselength)

	grams=[]
	for i in range(2,maxngram+1):
		grams.append(i)

	totals = {}

	lang = dict(am={},ge={},gu={},ti={})	
	mylang = dict(am=0,ge=0,gu=0,ti=0)
		
	overalltotal = [0,0] ; overallprecision = [0,0]
	overallaccuracy =[0,0] ; overallfscore = [0.00,0.00]
	totalngrams = copy.deepcopy(mylang)
	uniquengrams = copy.deepcopy(mylang)		
	overallrecallCFA = copy.deepcopy(mylang)
	overallrecallNBC = copy.deepcopy(mylang)
	mytotal = copy.deepcopy(lang)
	
	for i in mytotal:
		for j in grams:
			totals[j]=0
		mytotal[i]=copy.deepcopy(totals)

	overallconfusionCFA = copy.deepcopy(mytotal)
	overallconfusionNBC = copy.deepcopy(mytotal)

	for i in lang:
		for j in lang:
			totals[j]=0
		overallconfusionCFA[i]=copy.deepcopy(mylang)
		overallconfusionNBC[i]=copy.deepcopy(mylang)
	overallwrongsCFA = copy.deepcopy(overallconfusionCFA)
	overallwrongsNBC = copy.deepcopy(overallconfusionCFA)

	testing=[] #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
	for i in sampled:		
		testing.append(l.ngram(l.regex(i),1))	
	
	norepeat = set()
	frequencyTable=[] #[1,ት ,2,2,am,78,0.012987012987012988,0.0002563116749967961,1.559271820060032e-05,0.012987012987012988]
	for temp in model: #[am,ት ,2,2,78,1.0043572984749456,1.0009775171065494,0.012987012987012988]
		temps = temp.rstrip('\n').split(',')
		if float(percent)<1:
			if float(temps[7])<=float(percent):
				frequencyTable.append(temps)
				totalngrams[temps[0]]+=int(temps[3])
				if temps[1] not in norepeat:
					uniquengrams[temps[0]]+=1					
					norepeat.add(temps[1])
		elif int(lowfreq)!=0: 
			if int(temps[2])>lowfreq:
				frequencyTable.append(temps)
				totalngrams[temps[0]]+=int(temps[3])
				if temps[1] not in norepeat:
					uniquengrams[temps[0]]+=1					
					norepeat.add(temps[1])
		else:
			frequencyTable.append(temps)
			totalngrams[temps[0]]+=int(temps[3])
			if temps[1] not in norepeat:
				uniquengrams[temps[0]]+=1					
				norepeat.add(temps[1])			

	
	print ('Creating language dictionaries ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	l.overallmyclassifier(testing,frequencyTable,grams,overallwrongsCFA,overalltotal,overallrecallCFA,uniquengrams,overallwrongsNBC,overallrecallNBC,totalngrams)

	print ('Performing classifications ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	for i in overallconfusionCFA:
		for j in overallconfusionCFA[i]:
			if i==j:
				overallconfusionCFA[i][j]=overallrecallCFA[j]
				overallconfusionNBC[i][j]=overallrecallNBC[j]
			else:
				overallconfusionCFA[i][j]=overallwrongsCFA[i][j]
				overallconfusionNBC[i][j]=overallwrongsNBC[i][j]
	
	print ('overallconfusionCFA {}'.format(overallconfusionCFA))
	print ('overallconfusionNBC {}'.format(overallconfusionNBC))

	for i in lang:
		numerator=0 ; denominator=0
		n = 0 ; d = 0
		for j in overallconfusionCFA:
			if i==j: numerator += overallconfusionCFA[j][i] ; n += overallconfusionNBC[j][i]			
			denominator+= overallconfusionCFA[j][i]
			d += overallconfusionNBC[j][i]
		overallprecision[0]+=(numerator/denominator) if denominator!=0 else 0
		overallprecision[1]+=(n/d) if d!=0 else 0
	overallprecision[0]/=4
	overallprecision[1]/=4

	for x in overallconfusionCFA:
		numerator=0 ; denominator=0
		n = 0 ; d = 0
		for y in lang:
			if x==y: numerator += overallconfusionCFA[x][y]; n += overallconfusionNBC[x][y]				
			denominator+= overallconfusionCFA[x][y]
			d += overallconfusionNBC[x][y]
		overallrecallCFA[x]=(numerator/denominator) if denominator!=0 else 0
		overallrecallNBC[x]=(n/d) if d!=0 else 0
		overallaccuracy[0]+=numerator
		overallaccuracy[1]+=n
	overallaccuracy[0]/=overalltotal[0]
	overallaccuracy[1]/=overalltotal[1]
	
	overallfscore[0] = 2*((overallprecision[0]*(sum(overallrecallCFA.values())/4))/(overallprecision[0]+(sum(overallrecallCFA.values())/4))) if (overallprecision[0]!=0.00 or sum(overallrecallCFA.values()))!=0.00 else 0
	overallfscore[1] = 2*((overallprecision[1]*(sum(overallrecallNBC.values())/4))/(overallprecision[1]+(sum(overallrecallNBC.values())/4))) if (overallprecision[1]!=0.00 or sum(overallrecallNBC.values()))!=0.00 else 0
	
	print ('Generating performance metrices - precision, recall and f-score ...  \t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	print ('\n'); print ('-'*100)
	print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
	print ('-'*100)
	print ('{:<15}\t|{}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format('CFA (2,3,4,5)',overalltotal[0],overallaccuracy[0],overallprecision[0],(sum(overallrecallCFA.values())/4),overallfscore[0]))
	print ('{:<15}\t|{}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format('NBC (2,3,4,5)',overalltotal[1],overallaccuracy[1],overallprecision[1],(sum(overallrecallNBC.values())/4),overallfscore[1]))
	print ('-'*100)

	print ('\nGenerating clasification performance results ...  \t\t\t{}'.format(l.timer(mytime)))
	print ('\nStarted:', started)
	ended = datetime.datetime.now()
	print ('End    :', ended)
	print ('Elapsed: {}'.format(l.timer(started)))

def main():
	os.system('clear') # on linux 
	choice=1; phraselength=0;percent=0;lowfreq=0
	while choice!=0:
		print ('\n')
		print ('='*100)
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION'.center(100,' '))
		print ('-'*100)  
		try:			
			choice = int(input('\nPress 1 to classify [0 to exit] :   '))

			if choice==0:
				return
			else:
				percent = float(input('\n1. Enter a percentage as 0.xx to select the top x frequent items of the model :   '))
				phraselength = int(input('2. Insert between 1 and 10 to set the test phrase length from testing files   :   '))
				if float(percent)==1:
					lowfreq = int(input('3. Enter 1 to 5 not to consider lowest counts in the model [0 to consider all]:   '))
				else:
					lowfreq=0

				if phraselength>10 or phraselength<1 or percent<=0 or percent>1:
					print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
				else:
					classification(phraselength,percent,lowfreq)
		except ValueError:
			print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
			continue

if __name__ == '__main__':
	main()