import os ; import sys ; import re ; import glob ; import string ; import datetime ; import copy ; import decimal ; import langid as l

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
	#modularize classifier.py in to functions - move functions in to another file

def classification(ct,readsampled,vocabulary,mod,frequencyDict,uniquengrams,totalngrams,phraselength=25,lines=0,maxg=5):
	
	testing = readsampled[0]
	averagebyte = int(readsampled[1])
	averagecharacters = int(readsampled[2])
	phrases = int(readsampled[3])

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

	mytime = datetime.datetime.now()

	l.overallmyclassifier(testing,frequencyDict,overallwrongs,overalltotal,overallrecall,uniquengrams,totalngrams,phrases,vocabulary)
	
	print ('\tPerforming classifications ...  \t\t\t\t\t{}'.format(l.timer(mytime)))

	for i in overallconfusion['CFA']:
		for j in overallconfusion['CFA'][i]:
			if i==j:
				overallconfusion['CFA'][i][j]=overallrecall['CFA'][j]
				overallconfusion['NBC'][i][j]=overallrecall['NBC'][j]
			else:
				overallconfusion['CFA'][i][j]=overallwrongs['CFA'][i][j]
				overallconfusion['NBC'][i][j]=overallwrongs['NBC'][i][j]

	# print ('overallconfusion {}'.format(overallconfusion))
	
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
	
	path1='result/ov/'+str(ct)+'/'
	filename = mod+'.txt'
	r=open(os.path.join(path1, filename),'a+')

	print ('\nAverage length of test strings: {:,} word(s) / {:,} character(s) / {:,} bytes\tModel: {:,} lines.'.format(phraselength,averagecharacters,averagebyte,lines))
	print ('='*100)
	print ('{:<16}|{:<15}|{:<15}|{:<15}|{:<15}|{:<15}'.format('Ngrams','Observations','Accuracy','Precision','Recall','F-score'))
	print ('-'*100)	
	for i in base:
		r.write(str(i)+","+str(ct)+","+str(mod)+","+str(phraselength)+","+str(overalltotal[i])+","+str(overallaccuracy[i])+","+str(overallprecision[i])+","+str(sum(overallrecall[i].values())/maxofg)+","+str(overallfscore[i])+str('\r\n'))
		print ('{:<3} {:<10}\t|{:,}\t\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}\t|{:10.4f}'.format(i,'(2,3,4,5)',overalltotal[i],overallaccuracy[i],overallprecision[i],(sum(overallrecall[i].values())/maxofg),overallfscore[i]))
	print ('-'*100)
	r.close()

def main():
	os.system('clear') # on linux 
	choice=1; phraselength=0 ; modeltype = {1:'bl', 2:'by', 3:'fl', 4:'in', 5:'il'}
	while choice!=0:
		
		print ('\n\n{}'.format('='*100))
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - OVERALL TESTER'.center(100,' '))
		print ('-'*100)  
		
		started = datetime.datetime.now()

		for modelselector in range(1,7):
			
			wordbased=0 ; phraselength=0 ; infinity=0 ; location=0
			
			if modelselector==6: choice=0;break
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

				path1='result/ov/'+str(ct)+'/'
				filename = mod+'.txt'
				if os.path.isfile(os.path.join(path1,filename)): os.remove(os.path.join(path1,filename))
				
				path='models/'+str(ct)+'/'
				print ('-'*100) 
				print ('\nFiles {}{} located and opened ...  \t\t\t{}'.format(path,filename,l.timer(started)))
				params = [] ; params=l.readmodel(path,mod,frequencyDict,totalngrams,uniquengrams)
				frequencyDict = params[0] ; uniquengrams = params[1] ; lines=params[5]
				totalngrams = params[2] ; maxg=params[3] ; vocabulary=params[4]
				
				path2='samples/'
				for phraselength in  phrases:
					s=open(os.path.join(path2,str(ct)+'.txt'),'r') ; sample = s.readlines() ; s.close() ; readsampled=[]
					readsampled = l.readsample(sample,phraselength,wordbased,location,infinity)				
					classification(ct,readsampled,vocabulary,mod,frequencyDict,uniquengrams,totalngrams,phraselength,lines,maxg)
			else:
				print ('\nStarted:', started)
				ended = datetime.datetime.now()
				print ('End    :', ended)
				print ('Elapsed: {}'.format(l.timer(started)))

if __name__ == '__main__':
	main()