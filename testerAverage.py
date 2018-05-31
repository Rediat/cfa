import os ; import sys ; import re ; import glob
import string ; import datetime ; import decimal
import copy ; import langid as l

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
	#modularize classifier.py in to functions - move functions in to another file
	
def classification(ct,readsampled,vocabulary,mod,frequencyDict,uniquengrams,totalngrams,phraselength,wordbased=0,location=0,infinity=0,maxg=5,lines=0):

	#*************************** START Reading Files ************************************
	# started = datetime.datetime.now()
	
	# print ('\nFiles {} loaded to memory ...  \t\t\t\t\t\t{}'.format('sample.txt',l.timer(started)))
	mytime = datetime.datetime.now()
	print ('Opening relevant files ...  \t\t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	testing = readsampled[0]
	averagebyte = int(readsampled[1])
	averagecharacters = int(readsampled[2])
	phrases = int(readsampled[3])

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

	# print ('Creating language dictionaries ...  \t\t\t\t\t\t{}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	l.myclassifier(testing,frequencyDict,grams,wrongs,totaltests,myrecall,total,uniquengrams,totalngrams,phrases,vocabulary)
	
	print ('\tPerforming classifications ...  \t\t\t\t\t{}'.format(l.timer(mytime)))
	# mytime = datetime.datetime.now()

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

	path='result/av/'+str(ct)+'/'
	filename=mod+'.txt'
	r=open(os.path.join(path, filename),'a+')
	
	for i in classifiers:
		print ('\nAverage length of test strings: {:,} word(s) / {:,} character(s) / {:,} bytes\tModel: {:,} lines.'.format(phraselength,averagecharacters,averagebyte,lines))
		print ('='*100)
		print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
		print ('-'*100)		
		
		for g in grams:
			print ('{:<3} {:<10}\t|{:,}\t\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%'.format(i,g,totaltests[i][g],accuracy[i][g]*100,precision[i][g]*100,recall[i][g]*100,fscore[i][g]*100))
			r.write(str(i)+","+str(ct)+","+str(mod)+","+str(phraselength)+","+str(totaltests[i][g])+","+str(accuracy[i][g])+","+str(precision[i][g])+","+str(recall[i][g])+","+str(fscore[i][g])+","+str(g)+str('\r\n'))
		print ('-'*100)
		
		print ('{:<3} {:<10}\t|{:,}\t\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%\t|{:10.2f}%'.format(i,'(2,3,4,5)',averagetotal[i],averageaccuracy[i]*100,averageprecision[i]*100,averagerecall[i]*100,averagefscore[i]*100))
		print ('-'*100)
	r.close()

def main():	
	os.system('clear')
	choice=1; phraselength=0 ; modeltype = {1:'bl', 2:'by', 3:'fl', 4:'in', 5:'il'}
	
	while choice!=0:
		
		print ('\n\n{}'.format('='*100))
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - N-GRAMS TESTER'.center(100,' '))
		print ('-'*100)	

		started = datetime.datetime.now()

		for modelselector in range(4,7):

			wordbased=0 ; phraselength=0 ; infinity=0 ; location=0

			if modelselector==6: choice=0 ; break

			if modelselector<=0 or modelselector>6:
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
			
			os.system('clear') # on linux 
			started = datetime.datetime.now()
			phrases=[1,2,3,4,5,10,15,20,25]
			
			for ct in range(1,11):
				
				lang = dict(am={},ge={},gu={},ti={})
				mylang = dict(am=0,ge=0,gu=0,ti=0)
				totalngrams = copy.deepcopy(mylang)
				frequencyDict = copy.deepcopy(lang)
				uniquengrams = copy.deepcopy(mylang)

				path1='result/av/'+str(ct)
				filename = mod+'.txt'
				if os.path.isfile(os.path.join(path1,filename)): os.remove(os.path.join(path1,filename))
				
				path='models/'+str(ct)+'/'
				print ('-'*100) 
				print ('\nFiles {}{} located and opened ...  \t\t\t{}'.format(path,filename,l.timer(started)))

				params=l.readmodel(path,mod,frequencyDict,totalngrams,uniquengrams,)
				frequencyDict = params[0]; uniquengrams = params[1] ; lines=params[5]
				totalngrams = params[2]; maxg=params[3]; vocabulary=params[4]

				path2='samples/'
				for phraselength in  phrases:
					s=open(os.path.join(path2,str(ct)+'.txt'),'r') ; sample = s.readlines() ; s.close()
					readsampled = l.readsample(sample,phraselength,wordbased,location,infinity)	
					classification(ct,readsampled,vocabulary,mod,frequencyDict,uniquengrams,totalngrams,phraselength,wordbased,location,infinity,maxg,lines)
			else:
				print ('\nStarted:', started)
				ended = datetime.datetime.now()
				print ('End    :', ended)
				print ('Elapsed: {}'.format(l.timer(started)))

if __name__ == '__main__': 	main()