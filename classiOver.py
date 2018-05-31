import os ; import sys ; import re ; import glob
import string ; import datetime ; import decimal
import copy ; import langid as l

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
	#modularize classifier.py in to functions - move functions in to another file
	
# def classification(modeltype,phraselength=25,percent=1,lowfreq=0,wordbased=0,location=0):
def classification(frequencyDict,uniquengrams,totalngrams,phraselength=25,wordbased=0,location=0,infinity=0,maxg=5):

	#*************************** START Reading Files ************************************
	started = datetime.datetime.now()
	
	s=open('sample.txt','r') #, encoding = 'utf8' )

	print ('-'*100) 
	print ('\nFiles {} loaded to memory ...  \t\t\t\t\t\t{}'.format('sample.txt',l.timer(started)))
	mytime = datetime.datetime.now()
	print ('Opening relevant files ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	# model = f.readlines()
	#matrix = m.read()
	print ('Reading language models ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	sample = s.readlines()
	# f.close()
	s.close()
	#m.close()
	#*************************** END Reading Files ***************************************
	print ('Reading test strings ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	readsampled= l.readsample(sample,phraselength)
	sampled = readsampled[0]
	averagebyte = int(readsampled[1])
	averagecharacters = int(readsampled[2])

	testing=[] #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]

	temp=[] ; phrases = 0
	for i in sampled:
		if wordbased==0:
			testing.append(l.ngram(l.regex(i),1))
			phrases+=1
		else:
			temp = l.regex(i)[1].split()
			wordlist = []
			for n in temp:
				if location==0:
					wordlist.extend(l.ngram([i[0],n],1,location,infinity)[1])
				else:
					wordlist.extend(l.ngram([i[0],n],1,location,infinity)[1])
			testing.append([i[0],wordlist])
			phrases+=1

	grams=[]
	for i in range(2,maxg+1):
		grams.append(i)
	
	lang = dict(am={},ge={},gu={},ti={})	
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

	# print (testing);return
	print ('Creating language dictionaries ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	l.myclassifier(testing,frequencyDict,grams,wrongs,totaltests,myrecall,total,uniquengrams,totalngrams,phrases)
	
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
		print ('\nAverage length of test strings: {:,} word(s) / {:,} character(s) / {:,} bytes'.format(phraselength,averagecharacters,averagebyte))
		print ('='*100)
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
	os.system('clear')
	selection=1; modeltype = {1:'B', 2:'I', 3:'L', 4:'N', 5:'T'}
	# B. The Model is based on Byteorder Ngrams.
	# I. The Model is based on Infinitigrams without location features.
	# L. The Model is based on Infinitigrams with location features.
	# N. The Model is based on #2 above, for top n% of most frequent words.   
	# T. The Model is based on #3 above, for top n% of most frequent words.:
	while selection!=0:
		choice=1
		print ('\n\n{}'.format('='*100))
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - CLASSIFIER'.center(100,' '))
		print ('-'*100)	

		started = datetime.datetime.now()
		percent=1;lowfreq=0;location=0; wordbased=0

		lang = dict(am={},ge={},gu={},ti={})
		mylang = dict(am=0,ge=0,gu=0,ti=0)
		totalngrams = copy.deepcopy(mylang)
		frequencyDict = copy.deepcopy(lang)
		uniquengrams = copy.deepcopy(mylang)	
		
		modelselector = int(input('\nSelect Model type number below: \n\n   1. The Model is based on Byteorder Ngrams. \n   2. The Model is based on Infinitigrams without location features. \n   3. The Model is based on Infinitigrams with location features. \n   4. The Model is based on #2 above, for top n% of most frequent words. \n   5. The Model is based on #3 above, for top n% of most frequent words. \n   6. Exit.:   '))
		if modelselector==6: selection=0;break		
		elif modelselector<4 and modelselector>0:
			percent = float(input('\nEnter a percentage as 0.xx to select the top x frequent items of the model :   '))
		if float(percent)==1 and modelselector<4:
			lowfreq = int(input('Enter 1 to 5 not to consider lowest counts in the model [0 to consider all]:   '))			
		if percent<=0 or percent>1 or location<0 or modelselector<=0 or modelselector>6:
			print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
			pause=input(''); print('{}'.format(pause)) ; continue
		else:
			if modeltype[modelselector]=='I': 
				wordbased=1 ; location=0 ; infinity=1 ; mod='I'
			elif modeltype[modelselector]=='L': 
				wordbased=1 ; location=1 ; infinity=1 ; mod='L'
			elif modeltype[modelselector]=='N': 
				wordbased=1 ; location=0 ; infinity=1 ; mod='N'
			elif modeltype[modelselector]=='T': 
				wordbased=1 ; location=1 ; infinity=1 ; mod='T'
			else: 
				wordbased=0 ; location=0 ; mod=modeltype[modelselector]
			
			path='models/'+mod
			f=open(os.path.join(path, 'model.txt'),'r')

			print ('-'*100) 
			print ('\nFiles {}/{} located and opened ...  \t\t\t{}'.format(path,'model.txt',l.timer(started)))
			# mytime = datetime.datetime.now()
			# print ('Opening relevant files ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
			# mytime = datetime.datetime.now()				
			model = f.readlines()

			params=l.readmodel(model,frequencyDict,totalngrams,uniquengrams,percent,lowfreq)
			frequencyDict = params[0]; uniquengrams = params[1];totalngrams = params[2];top=params[3];maxg=params[4]
			
			# if os.path.isfile('t.txt'): os.remove('t.txt') ; t=open('t.txt', 'a+')
			# for i in lang:
			# 	for j in frequencyDict[i].keys():
			# 		t.write(str(i)+','+ str(j)+','+ str(frequencyDict[i][j]['gram'])+','+ str(frequencyDict[i][j]['freq'])+','+ str(frequencyDict[i][j]['ovFreq'])+str('\r\n'))
			# t.close()

		modelselected = {	1:' Model is based on Byteorder Ngrams. Considered {}%, frequencies > {}. ',
							2:' Model is based on Infinitigrams without location features. Considered {}%, frequencies > {}. ', 
							3:' Model is based on Infinitigrams with location features. Considered {}%, frequencies > {}. ',
							4:' Model is based on Infinitigrams without location features, for top {}% of most frequent words. ', 
							5:' Model is based on Infinitigrams with location features, for top {}% of most frequent words. '}
		
		os.system('clear') # on linux 
		while choice!=0:
			phraselength=0 ; infinity=0
			print ('\n\n{}'.format('='*100))
			print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - CLASSIFIER'.center(100,' '))
			print ('-'*100)
			if modelselector<4:
				print (modelselected[modelselector].format(percent*100,lowfreq).center(100,'*'))
			else:
				print (modelselected[modelselector].format(top*100).center(100,'*'))
			try:
				choice = int(input('\nPress 1 to classify 2 to change model [0 to exit] :   '))

				if choice==0: selection=0 ; break
				elif choice==2: choice=0; break
				else:
					phraselength = int(input('\nInsert between 1 and 25 to set the test phrase length from testing files   :   '))
					if phraselength>25 or phraselength<1:
						print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
					else:
						classification(frequencyDict,uniquengrams,totalngrams,phraselength,wordbased,location,infinity,maxg)

			except ValueError:
				print ('\n\nPlease check your entry on percent, ngram value, and/or phrase length')
				continue

if __name__ == '__main__': 	main()