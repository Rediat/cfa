import os ; import sys ; import re ; import glob
import string ; import datetime ; import decimal
import copy ; import langid as l

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
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
	print ('Opening relevant files ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	print ('Reading language models ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	#*************************** END Reading Files ***************************************
	print ('Reading test strings ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	# testing=[] #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]

	grams=[]
	for i in range(2,maxg+1):
		grams.append(i)
	
	lang = dict(am={},ge={},gu={},ti={})	
	base = {'CFA':{},'NBC':{}}
	wrongs = copy.deepcopy(base)
	mytotals = copy.deepcopy(base)
	fscore = copy.deepcopy(base)
	mytotal = copy.deepcopy(lang)

	maxofg =  len(lang)
	averaging = len(grams)

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

	print ('Creating language dictionaries ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	l.myclassifier(testing,frequencyDict,grams,wrongs,totaltests,myrecall,total,uniquengrams,totalngrams,phrases,vocabulary)
	
	print ('\tPerforming classifications ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
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

			precision['CFA'][g]+=(numerator/denominator/maxofg) if denominator!=0 else 0
			precision['NBC'][g]+=(n/d/maxofg) if d!=0 else 0
		
		for x in confusion['CFA']:
			numerator=0 ; denominator=0	
			n = 0 ; d = 0
			for y in lang:
				if x==y: numerator += confusion['CFA'][x][y][g]; n += confusion['NBC'][x][y][g]			
				denominator+= confusion['CFA'][x][y][g]
				d += confusion['NBC'][x][y][g]

			recall['CFA'][g]+=(numerator/denominator/maxofg) if denominator!=0 else 0
			recall['NBC'][g]+=(n/d/maxofg) if d!=0 else 0
			accuracy['CFA'][g]+=numerator
			accuracy['NBC'][g]+=n

		accuracy['CFA'][g]/=total['CFA'][g] if total['CFA'][g]!=0 else 1
		accuracy['NBC'][g]/=total['NBC'][g] if total['NBC'][g]!=0 else 1

		averageaccuracy['CFA']+=accuracy['CFA'][g]/averaging
		averageaccuracy['NBC']+=accuracy['NBC'][g]/averaging

		averagetotal['CFA']+=totaltests['CFA'][g]
		averagetotal['NBC']+=totaltests['NBC'][g]

		averageprecision['CFA']+=precision['CFA'][g]/averaging
		averageprecision['NBC']+=precision['NBC'][g]/averaging

		averagerecall['CFA']+=recall['CFA'][g]/averaging
		averagerecall['NBC']+=recall['NBC'][g]/averaging

	for g in grams:		
		fscore['CFA'][g] = 2*((precision['CFA'][g]*recall['CFA'][g])/(precision['CFA'][g]+recall['CFA'][g])) if (precision['CFA'][g]!=0.00 or recall['CFA'][g])!=0.00 else 0
		fscore['NBC'][g] = 2*((precision['NBC'][g]*recall['NBC'][g])/(precision['NBC'][g]+recall['NBC'][g])) if (precision['NBC'][g]!=0.00 or recall['NBC'][g])!=0.00 else 0
		averagefscore['CFA'] +=fscore['CFA'][g]/averaging
		averagefscore['NBC'] +=fscore['NBC'][g]/averaging

	print ('Generating performance metrices - precision, recall and f-score ...  \t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	for i in classifiers:
		print ('\nAverage length of test strings: {:,} word(s) / {:,} character(s) / {:,} bytes\tModel: {:,} lines.'.format(phraselength,averagecharacters,averagebyte,lines))
		print ('='*100)
		print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
		print ('-'*100)
		
		for g in grams:
			print ('{:<3} {:<10}\t|{:,}\t\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%'.format(i,g,totaltests[i][g],accuracy[i][g]*100,precision[i][g]*100,recall[i][g]*100,fscore[i][g]*100))
		print ('-'*100)
		
		print ('{:<3} {:<10}\t|{:,}\t\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%'.format(i,'(2,3,4,5)',averagetotal[i],averageaccuracy[i]*100,averageprecision[i]*100,averagerecall[i]*100,averagefscore[i]*100))
		print ('-'*100)

	print ('\nGenerating clasification performance results ...  \t\t\t\t{}'.format(l.timer(mytime)))
	print ('\nStarted:', started)
	ended = datetime.datetime.now()
	print ('End    :', ended)
	print ('Elapsed: {}'.format(l.timer(started)))

def main():	
	os.system('clear')
	selection=1; modeltype = {1:'bl', 2:'by', 3:'fl', 4:'in', 5:'il'}
	while selection!=0:
		choice=1 ; wordbased=0 ; phraselength=0 ; infinity=0
		print ('\n\n{}'.format('='*100))
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - CLASSIFIER'.center(100,' '))
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
		
		if modelselector==6: selection=0;break		

		if location<0 or modelselector<=0 or modelselector>6 or ct<=0 or ct>10:
			print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
			pause=input(''); print('{}'.format(pause)) ; break
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

			params=l.readmodel(path,mod,frequencyDict,totalngrams,uniquengrams,)
			frequencyDict = params[0]; uniquengrams = params[1] ; lines=params[5]
			totalngrams = params[2]; maxg=params[3]; vocabulary=params[4]

		modelselected = {	1:' The Model is based on Fixed Length N-grams without location features - Baseline [bl] on test {}. ',
							2:' The Model is based on source text - Byteorder Ngrams [by] on test {}. ', 
							3:' The Model is based on Fixed Length N-grams with location features [fl] on test {}. ', 
							4:' The Model is based on Infiniti-grams without location features [in] on test {}. ',
							5:' The Model is based on Infiniti-grams with location features. [il] on test {}. '
						}

		os.system('clear') # on linux 
		while choice!=0:
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

if __name__ == '__main__': 	main()