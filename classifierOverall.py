import os
import sys ; import re ; import glob ; import string ; import datetime ; import copy ; import decimal ; import langid as l

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
	#Consider multilingual testing samples
	#modularize classifier.py in to functions - move functions in to another file

def classification(ct,readsampled,vocabulary,frequencyDict,uniquengrams,totalngrams,phraselength=25,wordbased=0,location=0,infinity=0,maxg=5,lines=0):
	#*************************** START Reading Files ************************************
	started = datetime.datetime.now()
	
	testing = readsampled[0]
	averagebyte = int(readsampled[1])
	averagecharacters = int(readsampled[2])
	phrases = int(readsampled[3])

	print ('-'*100) 
	# print ('\nFiles {} loaded to memory ...  \t\t\t\t\t\t{}'.format(path+filename,l.timer(started)))
	mytime = datetime.datetime.now()
	
	print ('Reading language models ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	#*************************** END Reading Files ***************************************
	print ('Reading test strings ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	grams=[]
	for i in range(2,maxg+1):
		grams.append(i)

	totals = {}

	lang = dict(am={},ge={},gu={},ti={})
	mylang = dict(am=0,ge=0,gu=0,ti=0)
	maxofg = len(lang)

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

	print ('Creating language dictionaries ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	l.overallmyclassifier(testing,frequencyDict,overallwrongs,overalltotal,overallrecall,uniquengrams,totalngrams,phrases,vocabulary)
	
	print ('Performing classifications ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	# print (overallwrongs);return

	for i in overallconfusion['CFA']:
		for j in overallconfusion['CFA'][i]:
			if i==j:
				overallconfusion['CFA'][i][j]=overallrecall['CFA'][j]
				overallconfusion['NBC'][i][j]=overallrecall['NBC'][j]
			else:
				overallconfusion['CFA'][i][j]=overallwrongs['CFA'][i][j]
				overallconfusion['NBC'][i][j]=overallwrongs['NBC'][i][j]

	print ('overallconfusion {}'.format(overallconfusion))
	
	for i in lang:
		numerator=0 ; denominator=0
		n = 0 ; d = 0
		for j in overallconfusion['CFA']:
			if i==j: numerator += overallconfusion['CFA'][j][i] ; n += overallconfusion['NBC'][j][i]			
			denominator+= overallconfusion['CFA'][j][i]
			d += overallconfusion['NBC'][j][i]

		overallprecision['CFA']+=(numerator/denominator) if denominator!=0 else 0
		overallprecision['NBC']+=(n/d) if d!=0 else 0
	
	overallprecision['CFA']/=maxofg
	overallprecision['NBC']/=maxofg

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
		overallfscore[i] = 2*((overallprecision[i]*(sum(overallrecall[i].values())/maxofg))/(overallprecision[i]+(sum(overallrecall[i].values())/maxofg))) if (overallprecision[i]!=0.00 or sum(overallrecall[i].values()))!=0.00 else 0
	
	print ('Generating performance metrices - precision, recall and f-score ...  \t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	
	print ('\nAverage length of test strings: {:,} word(s) / {:,} character(s) / {:,} bytes\tModel: {:,} lines.'.format(phraselength,averagecharacters,averagebyte,lines))
	print ('='*100)
	print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
	print ('-'*100)
	for i in base:
		print ('{:<3} {:<10}\t|{:,}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format(i,'(2,3,4,5)',overalltotal[i],overallaccuracy[i],overallprecision[i],(sum(overallrecall[i].values())/maxofg),overallfscore[i]))

	print ('-'*100)
	print ('\nGenerating clasification performance results ...  \t\t\t{}'.format(l.timer(mytime)))
	print ('\nStarted:', started)
	ended = datetime.datetime.now()
	print ('End    :', ended)
	print ('Elapsed: {}'.format(l.timer(started)))

def main():
	os.system('clear') # on linux 
	selection=1; phraselength=0 ; modeltype = {1:'bl', 2:'by', 3:'fl', 4:'in', 5:'il'} 
	while selection!=0:
		choice=1
		print ('\n')
		print ('='*100)
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION'.center(100,' '))
		print ('-'*100)  
		
		started = datetime.datetime.now()
		location=0; wordbased=0

		lang = dict(am={},ge={},gu={},ti={})
		mylang = dict(am=0,ge=0,gu=0,ti=0)
		totalngrams = copy.deepcopy(mylang)
		frequencyDict = copy.deepcopy(lang)
		uniquengrams = copy.deepcopy(mylang)

		ct = int(input('\nSelect Test number  - 1 to 10 :   '))
		modelselector = int(input('\nSelect Model type number below: \n\n   1. The Model is based on Fixed Length N-grams without location features - Baseline [BL]. \n   2. The Model is based on source text - Byteorder N-grams [BY]. \n   3. The Model is based on Fixed Length N-grams with location features [FL]. \n   4. The Model is based on Infiniti-grams without location features [IN]. \n   5. The Model is based on Infiniti-grams with location features [IL]. \n   6. Exit.:   '))
		
		if modelselector==6: choice=0;break		

		if location<0 or modelselector<=0 or modelselector>6 or ct<=0 or ct>10:
			print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
			pause=input(''); print('{}'.format(pause)) ; continue
		else:
			if modeltype[modelselector]=='bl':
				wordbased=1 ; location=0 ; infinity=0 ; mod='bl'
			elif modeltype[modelselector]=='fl': 
				wordbased=1 ; location=1 ; infinity=0 ; mod='fl'
			elif modeltype[modelselector]=='in': 
				wordbased=1 ; location=0 ; infinity=1 ; mod='in'
			elif modeltype[modelselector]=='il': 
				wordbased=1 ; location=1 ; infinity=1 ; mod='il'
			else: 
				wordbased=0 ; location=0 ; mod=modeltype[modelselector]
			
			path='models/'+str(ct)
			filename = mod+'.txt'
			print ('-'*100) 
			print ('\nFiles {}/{} located and opened ...  \t\t\t{}'.format(path,filename,l.timer(started)))

			params=l.readmodel(path,mod,frequencyDict,totalngrams,uniquengrams)
			frequencyDict = params[0]; uniquengrams = params[1] ; lines=params[5]
			totalngrams = params[2]; maxg=params[3];vocabulary=params[4]

		modelselected = {	1:' The Model is based on Fixed Length N-grams without location features - Baseline [bl] on test {}. ',
						2:' The Model is based on source text - Byteorder Ngrams [by] on test {}. ', 
						3:' The Model is based on Fixed Length N-grams with location features [fl] on test {}. ', 
						4:' The Model is based on Infiniti-grams without location features [in] on test {}. ',
						5:' The Model is based on Infiniti-grams with location features. [il] on test {}. '
					}
		os.system('clear')
		selection=1 # on linux 
		while choice!=0:
			phraselength=0 ; infinity=0
			print ('\n\n{}'.format('='*100))
			print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - CLASSIFIER'.center(100,' '))
			print ('-'*100)
			print (modelselected[modelselector].format(ct).center(100,'*'))
			
			try:
				choice = int(input('\nPress 1 to classify 2 to change model [0 to exit] :   '))
				if choice==0: selection=0 ; break
				elif choice==2: choice=0; break
				else:
					phraselength = int(input('\nInsert between 1 and 25 to set the test phrase length from testing files   :   '))
					if phraselength>25 or phraselength<1:
						print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
					else:
						path2='samples/'
						s=open(os.path.join(path2,str(ct)+'.txt'),'r') ; sample = s.readlines() ; s.close()
						readsampled = l.readsample(sample,phraselength,wordbased,location,infinity)
						classification(ct,readsampled,vocabulary,frequencyDict,uniquengrams,totalngrams,phraselength,wordbased,location,infinity,maxg,lines)
			except ValueError:
				print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
				continue

if __name__ == '__main__':
	main()