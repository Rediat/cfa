import os
import sys
import re
import glob
import string
import datetime
import copy
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

	print ('-'*81) 
	print ('\nOpening relevant files ...  {}'.format(l.timer(started)))
	mytime = datetime.datetime.now()
	
	model = f.readlines()
	#matrix = m.read()
	print ('\nReading language models ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	sample = s.readlines()
	f.close()
	s.close()
	#m.close()
	#*************************** END Reading Files ***************************************
	print ('\nReading test strings ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	#you can control the phrase length here by indenting the line below
	 #[['am', 'እውነት', '1', '4', '82']]
	sampled= l.readsample(sample,phraselength)

	grams=[]
	for i in range(2,maxngram+1):
		grams.append(i)
	
	mylang = dict(am=0,ge=0,gu=0,ti=0)
	totalngrams = copy.deepcopy(mylang)
	uniquengrams = copy.deepcopy(mylang)

	lang = dict(am={},ge={},gu={},ti={})
	fscore = {'CFA':{},'NBC':{}}
	wrongs = copy.deepcopy(fscore)
	mytotals = copy.deepcopy(fscore)

	mytotal = copy.deepcopy(lang)
	
	for i in grams:
		fscore['CFA'][i]=0 ; fscore['NBC'][i]=0

	precision = copy.deepcopy(fscore)
	total = copy.deepcopy(fscore)
	recall = copy.deepcopy(fscore)
	accuracy = copy.deepcopy(fscore)

	totals = {}

	for i in mytotal:
		for j in grams:
			totals[j]=0
		mytotal[i]=copy.deepcopy(totals)

	mytotals['CFA'] = copy.deepcopy(mytotal)
	mytotals['NBC'] = copy.deepcopy(mytotal)		

	myrecall = copy.deepcopy(mytotals)
			
	# wrongs = {} #wrong classifications detail like amharic identified as guragigna
	for i in mytotal:
		wrongs['CFA'][i]=copy.deepcopy(mytotal)
		wrongs['NBC'][i]=copy.deepcopy(mytotal)

	confusion = copy.deepcopy(wrongs)

	testing=[] #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
	for i in sampled:		
		testing.append(l.ngram(l.regex(i),1))	

	# norepeat = set()
	frequencyTable=[] #[am,ት ,2,99,78,1.0000414864728955,1.0000109646985438,0.0063978286157425355]
	for temp in model:
		temps = temp.rstrip('\n').split(',')
		uniquengrams[temps[0]]+=1
		totalngrams[temps[0]]+=int(temps[3])
		if float(percent)<1:
			if float(temps[7])<=float(percent):
				frequencyTable.append(temps)
		elif int(lowfreq)!=0: 
			if int(temps[3])>lowfreq:
				frequencyTable.append(temps)
		else:
			frequencyTable.append(temps)			

	print ('\nCreating language dictionaries ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	l.myclassifier(testing,frequencyTable,grams,wrongs,mytotals,myrecall,total,uniquengrams,totalngrams)
	# myclassifier(testing,frequencyTable,grams,wrongs,mytotals,myrecall,total,uniquengrams,totalngrams):
	
	print ('\nPerforming classifications ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	for i in confusion['CFA']:
		for j in confusion['CFA'][i]:
			if i==j:
				confusion['CFA'][i][j]=myrecall['CFA'][j]
				confusion['NBC'][i][j]=myrecall['NBC'][j]
			else:
				confusion['CFA'][i][j]=wrongs['CFA'][i][j]
				confusion['NBC'][i][j]=wrongs['NBC'][i][j]		

	print ('overallconfusionNBC {}'.format(confusion['NBC']))

	for g in grams:
				
		for i in lang:
			numerator=0 ; denominator=0	
			n = 0 ; d = 0									
			for j in confusion['CFA']:
				if i==j: numerator += confusion['CFA'][j][i][g] ; n +=	confusion['NBC'][j][i][g]		
				denominator+= confusion['CFA'][j][i][g]
				d += confusion['NBC'][j][i][g]
			precision['CFA'][g]+=(numerator/denominator/4) if denominator!=0 else 0
			precision['NBC'][g]+=(n/d/4) if d!=0 else 0
		
		for x in confusion['CFA']:
			numerator=0 ; denominator=0	
			n = 0 ; d = 0
			for y in lang:
				if x==y: numerator += confusion['CFA'][x][y][g]; n += confusion['NBC'][x][y][g]			
				denominator+= confusion['CFA'][x][y][g]
				d += confusion['NBC'][x][y][g]
			recall['CFA'][g]+=(numerator/denominator/4) if denominator!=0 else 0
			recall['NBC'][g]+=(n/d/4) if d!=0 else 0
			accuracy['CFA'][g]+=numerator
			accuracy['NBC'][g]+=n
		accuracy['CFA'][g]/=total['CFA'][g] if total['CFA'][g]!=0 else 1
		accuracy['NBC'][g]/=total['NBC'][g] if total['NBC'][g]!=0 else 1

	for g in grams:		
		fscore['CFA'][g] = 2*((precision['CFA'][g]*recall['CFA'][g])/(precision['CFA'][g]+recall['CFA'][g])) if (precision['CFA'][g]!=0.00 or recall['CFA'][g])!=0.00 else 0
		fscore['NBC'][g] = 2*((precision['NBC'][g]*recall['NBC'][g])/(precision['NBC'][g]+recall['NBC'][g])) if (precision['NBC'][g]!=0.00 or recall['NBC'][g])!=0.00 else 0

	print ('\nGenerating performance metrices - precission, recall and f-score ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	if os.path.isfile('result.txt'): os.remove('result.txt')
	# r=open('result.txt','a+')

	for i in ('CFA','NBC'):
		print ('\n'); print ('='*100)  
		print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
		print ('-'*100)
		for g in grams:
			print ('{:<3} {:<10}\t|{}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format(i,g,total[i][g],accuracy[i][g],precision[i][g],recall[i][g],fscore[i][g]))
		print ('-'*100)
		# r.write(str(g)+","+str(total['CFA'][g])+","+str(accuracy['CFA'][g])+","+str(precision['CFA'][g])+","+str(recall['CFA'][g])+","+str(fscore['CFA'][g])+str('\r\n'))
	# r.close()
	# print ("\nAllgrams\t{}\t\t{:10.4f}\t{:10.4f}\t{:10.4f}\t{:10.4f}".format(overalltotal[0],overallaccuracy[0],overallprecision[0],(sum(overallrecall.values())/4),overallfscore))
	print ('\nGenerating clasification performance results ...  {}'.format(l.timer(mytime)))

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
				percent = float(input('\n1. Enter a percentage as 0.xx to select the top x frequent items of the model:   '))
				phraselength = int(input('2. Insert one from 1 to 10 to set the test phrase length:   '))
				if float(percent)==1:
					lowfreq = int(input('3. Enter 1 to 5 not to consider in the model [0 to consider all]:   '))
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