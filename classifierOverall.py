import os
import sys
import re
import glob
import string
import datetime
import copy
import decimal
import langid as l

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
	#Consider multilingual testing samples
	#modularize classifier.py in to functions - move functions in to another file

def classification(phraselength,percent=1,lowfreq=0):

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
	totalngrams = copy.deepcopy(mylang)
	frequencyDict = copy.deepcopy(lang)
	uniquengrams = copy.deepcopy(mylang)

	base=dict(CFA={},NBC={})
	overallrecall = copy.deepcopy(base)
	for i in overallrecall:
		overallrecall[i] = copy.deepcopy(mylang)

	overalltotal = {'CFA':0,'NBC':0}
	overallprecision = copy.deepcopy(overalltotal)
	overallaccuracy = copy.deepcopy(overalltotal)
	overallfscore = copy.deepcopy(overalltotal)

	mytotal = copy.deepcopy(lang)
	
	for i in mytotal:
		for j in grams:
			totals[j]=0
		mytotal[i]=copy.deepcopy(totals)

	overallconfusion=copy.deepcopy(base)
	for i in overallconfusion:
		overallconfusion[i] = copy.deepcopy(mytotal)

	overallconfusion['CFA'] = copy.deepcopy(mytotal)
	overallconfusion['NBC'] = copy.deepcopy(mytotal)	

	for i in lang:
		for j in lang:
			totals[j]=0
		overallconfusion['CFA'][i]=copy.deepcopy(mylang)
		overallconfusion['NBC'][i]=copy.deepcopy(mylang)
	
	overallwrongs = copy.deepcopy(overallconfusion)

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
				frequencyDict[temps[0]][temps[1]]=copy.deepcopy(dict(freq=temps[3],ovFreq=temps[6]))
				totalngrams[temps[0]]+=int(temps[3])
				if temps[1] not in norepeat:
					uniquengrams[temps[0]]+=1
					norepeat.add(temps[1])
		
		elif int(lowfreq)!=0: 
			if int(temps[3])>lowfreq:
				frequencyTable.append(temps)
				frequencyDict[temps[0]][temps[1]]=copy.deepcopy(dict(freq=temps[3],ovFreq=temps[6]))
				totalngrams[temps[0]]+=int(temps[3])
				if temps[1] not in norepeat:
					uniquengrams[temps[0]]+=1					
					norepeat.add(temps[1])
		else:
			frequencyTable.append(temps)
			totalngrams[temps[0]]+=int(temps[3])
			frequencyDict[temps[0]][temps[1]]=copy.deepcopy(dict(freq=temps[3],ovFreq=temps[6]))
			if temps[1] not in norepeat:
				uniquengrams[temps[0]]+=1
				norepeat.add(temps[1])

	print ('Creating language dictionaries ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	l.overallmyclassifier(testing,frequencyDict,overallwrongs,overalltotal,overallrecall,uniquengrams,totalngrams)

	print ('Performing classifications ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	for i in overallconfusion['CFA']:
		for j in overallconfusion['CFA'][i]:
			if i==j:
				overallconfusion['CFA'][i][j]=overallrecall['CFA'][j]
				overallconfusion['NBC'][i][j]=overallrecall['NBC'][j]
			else:
				overallconfusion['CFA'][i][j]=overallwrongs['CFA'][i][j]
				overallconfusion['NBC'][i][j]=overallwrongs['NBC'][i][j]

	for i in lang:
		numerator=0 ; denominator=0
		n = 0 ; d = 0
		for j in overallconfusion['CFA']:
			if i==j: numerator += overallconfusion['CFA'][j][i] ; n += overallconfusion['NBC'][j][i]			
			denominator+= overallconfusion['CFA'][j][i]
			d += overallconfusion['NBC'][j][i]

		overallprecision['CFA']+=(numerator/denominator) if denominator!=0 else 0
		overallprecision['NBC']+=(n/d) if d!=0 else 0
	
	overallprecision['CFA']/=4
	overallprecision['NBC']/=4

	for x in overallconfusion['CFA']:
		numerator=0 ; denominator=0
		n = 0 ; d = 0
		for y in lang:
			if x==y: numerator += overallconfusion['CFA'][x][y]; n += overallconfusion['NBC'][x][y]				
			denominator+= overallconfusion['CFA'][x][y]
			d += overallconfusion['NBC'][x][y]

		overallrecall['CFA'][x]=(numerator/denominator) if denominator!=0 else 0
		overallrecall['NBC'][x]=(n/d) if d!=0 else 0
		overallaccuracy['CFA']+=numerator
		overallaccuracy['NBC']+=n

	overallaccuracy['CFA']/=overalltotal['CFA']
	overallaccuracy['NBC']/=overalltotal['NBC']
	
	for i in base:
		overallfscore[i] = 2*((overallprecision[i]*(sum(overallrecall[i].values())/4))/(overallprecision[i]+(sum(overallrecall[i].values())/4))) if (overallprecision[i]!=0.00 or sum(overallrecall[i].values()))!=0.00 else 0
	
	print ('Generating performance metrices - precision, recall and f-score ...  \t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	print ('\n'); print ('-'*100)
	print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
	print ('-'*100)
	for i in base:
		print ('{:<3} {:<10}\t|{:,}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format(i,'(2,3,4,5)',overalltotal[i],overallaccuracy[i],overallprecision[i],(sum(overallrecall[i].values())/4),overallfscore[i]))

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
				phraselength = int(input('2. Insert between 1 and 25 to set the test phrase length from testing files   :   '))
				if float(percent)==1:
					lowfreq = int(input('3. Enter 1 to n not to consider lowest counts in the model [0 to consider all]:   '))
				else:
					lowfreq=0

				if phraselength>25 or phraselength<1 or percent<=0 or percent>1:
					print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
				else:
					classification(phraselength,percent,lowfreq)
		except ValueError:
			print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
			continue

if __name__ == '__main__':
	main()