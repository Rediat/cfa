import os
import sys
import re
import glob
import string
import datetime
import copy
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
	print ('\nOpening relevant files ...  \t\t\t\t\t\t\t{}'.format(l.timer(started)))
	mytime = datetime.datetime.now()
	
	model = f.readlines()
	#matrix = m.read()
	print ('Reading language models ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	sample = s.readlines()
	f.close()
	s.close()
	#m.close()
	#*************************** END Reading Files ***************************************
	print ('Reading test strings ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	sampled= l.readsample(sample,phraselength)

	grams=[]
	for i in range(2,maxngram+1):
		grams.append(i)
	
	lang = dict(am={},ge={},gu={},ti={})
	mylang = dict(am=0,ge=0,gu=0,ti=0)
	totalngrams = copy.deepcopy(mylang)
	frequencyDict = copy.deepcopy(lang)
	uniquengrams = copy.deepcopy(mylang)	
	
	base = {'CFA':{},'NBC':{}}
	wrongs = copy.deepcopy(base)
	mytotals = copy.deepcopy(base)
	fscore = copy.deepcopy(base)

	mytotal = copy.deepcopy(lang)

	classifiers = {'CFA':0,'NBC':0}
	averageprecision = copy.deepcopy(classifiers)
	averageaccuracy = copy.deepcopy(classifiers)
	averagefscore = copy.deepcopy(classifiers)
	averagerecall = copy.deepcopy(classifiers)
	averagetotal = copy.deepcopy(classifiers)
	
	for i in grams:
		fscore['CFA'][i]=0 ; fscore['NBC'][i]=0

	precision = copy.deepcopy(fscore)
	total = copy.deepcopy(fscore)
	totaltests = copy.deepcopy(fscore) 
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
			
	#wrong classifications like amharic classified as guragigna
	for i in mytotal:
		wrongs['CFA'][i]=copy.deepcopy(mytotal)
		wrongs['NBC'][i]=copy.deepcopy(mytotal)

	confusion = copy.deepcopy(wrongs)

	testing=[] #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
	
	for i in sampled:		
		testing.append(l.ngram(l.regex(i),1))

	norepeat = set()
	frequencyTable=[] 
	for temp in model: #[am,ት ,2,2,78,1.0043572984749456,1.0009775171065494,0.012987012987012988]
		temps = temp.rstrip('\n').split(',')
		if float(percent)<1:
			if float(temps[7])<=float(percent):
				frequencyTable.append(temps)
				frequencyDict[temps[0]][temps[1]]=dict(gram=temps[2],freq=temps[3],ovFreq=temps[6])
				totalngrams[temps[0]]+=int(temps[3])
				if temps[1] not in norepeat:
					uniquengrams[temps[0]]+=1					
					norepeat.add(temps[1])

		elif int(lowfreq)!=0: 
			if int(temps[3])>lowfreq:
				frequencyTable.append(temps)
				frequencyDict[temps[0]][temps[1]]=dict(gram=temps[2],freq=temps[3],ovFreq=temps[6])
				totalngrams[temps[0]]+=int(temps[3])
				if temps[1] not in norepeat:
					uniquengrams[temps[0]]+=1					
					norepeat.add(temps[1])
		else:
			frequencyTable.append(temps)
			totalngrams[temps[0]]+=int(temps[3])
			frequencyDict[temps[0]][temps[1]]=dict(gram=temps[2],freq=temps[3],ovFreq=temps[6])

			if temps[1] not in norepeat:
				uniquengrams[temps[0]]+=1
				norepeat.add(temps[1])			

	print ('Creating language dictionaries ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	l.myclassifier(testing,frequencyDict,grams,wrongs,totaltests,myrecall,total,uniquengrams,totalngrams)
	
	print ('Performing classifications ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	for i in confusion['CFA']:
		for j in confusion['CFA'][i]:
			if i==j:
				confusion['CFA'][i][j]=myrecall['CFA'][j]
				confusion['NBC'][i][j]=myrecall['NBC'][j]
			else:
				confusion['CFA'][i][j]=wrongs['CFA'][i][j]
				confusion['NBC'][i][j]=wrongs['NBC'][i][j]

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

		averageaccuracy['CFA']+=accuracy['CFA'][g]/4
		averageaccuracy['NBC']+=accuracy['NBC'][g]/4

		averagetotal['CFA']+=totaltests['CFA'][g]
		averagetotal['NBC']+=totaltests['NBC'][g]

		averageprecision['CFA']+=precision['CFA'][g]/4
		averageprecision['NBC']+=precision['NBC'][g]/4

		averagerecall['CFA']+=recall['CFA'][g]/4
		averagerecall['NBC']+=recall['NBC'][g]/4

	for g in grams:		
		fscore['CFA'][g] = 2*((precision['CFA'][g]*recall['CFA'][g])/(precision['CFA'][g]+recall['CFA'][g])) if (precision['CFA'][g]!=0.00 or recall['CFA'][g])!=0.00 else 0
		fscore['NBC'][g] = 2*((precision['NBC'][g]*recall['NBC'][g])/(precision['NBC'][g]+recall['NBC'][g])) if (precision['NBC'][g]!=0.00 or recall['NBC'][g])!=0.00 else 0
		averagefscore['CFA'] +=fscore['CFA'][g]/4
		averagefscore['NBC'] +=fscore['NBC'][g]/4

	print ('Generating performance metrices - precision, recall and f-score ...  \t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	if os.path.isfile('result.txt'): os.remove('result.txt')
	# r=open('result.txt','a+')

	for i in classifiers:
		print ('\n'); print ('='*100)
		print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
		print ('-'*100)
		
		for g in grams:
			print ('{:<3} {:<10}\t|{:,}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format(i,g,totaltests[i][g],accuracy[i][g],precision[i][g],recall[i][g],fscore[i][g]))
		print ('-'*100)
		
		print ('{:<3} {:<10}\t|{:,}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format(i,'(2,3,4,5)',averagetotal[i],averageaccuracy[i],averageprecision[i],averagerecall[i],averagefscore[i]))
		print ('-'*100)

	print ('\nGenerating clasification performance results ...  \t\t\t\t{}'.format(l.timer(mytime)))
	print ('\nStarted:', started)
	ended = datetime.datetime.now()
	print ('End    :', ended)
	print ('Elapsed: {}'.format(l.timer(started)))

def main():
	os.system('clear') # on linux 
	choice=1; phraselength=0;percent=0;lowfreq=0
	while choice!=0:
		print ('\n\n{}'.format('='*100))
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
					lowfreq = int(input('3. Enter 1 to 5 not to consider lowest counts in the model [0 to consider all]:   '))
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