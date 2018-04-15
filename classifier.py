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
	#[Build classifier for Naive Bayes and Frequency Rank]
	#Create a file that execues modeler sampler and classifier one after the other execute.py
	#modularize classifier.py in to functions - move functions in to another file
	#measure performace based on number of words in sample query

def classification(phraselength):

	#*************************** START Reading Files ************************************

	started = datetime.datetime.now()
	maxngram = 5
	f=open('model.txt','r') #, encoding = 'utf8' )
	#m=open('metrix.txt','r', encoding = 'utf8' )
	s=open('sample.txt','r') #, encoding = 'utf8' )

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
	sampled=[] = l.readsample(sample,phraselength)

	grams=[]
	for i in range(2,maxngram+1):
		grams.append(i)

	precision = {}
	total = {}
	recall = {}

	for i in grams:
		precision[i]=0
		total[i] = 0		
		recall[i] =0

	totals = {}
	lang = dict(am={},ge={},gu={},ti={},no={})
	mytotal = dict(am={},ge={},gu={},ti={},no={})

	for i in mytotal:
		for j in grams:
			totals[j]=0
		mytotal[i]=copy.deepcopy(totals)
	
	myrecall = copy.deepcopy(mytotal)
			
	wrongs = {} #wrong classifications detail like amharic identified as guragigna
	for i in mytotal:
		wrongs[i]=copy.deepcopy(mytotal)

	confusion = copy.deepcopy(wrongs)

	testing=[] #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
	for i in sampled:		
		testing.append(l.ngram(l.regex(i),1))	

	frequencyTable=[] #[1,ት ,2,2,am,78,0.012987012987012988,0.0002563116749967961,1.848924388237143e-05]
	for temp in model:
		frequencyTable.append(temp.rstrip('\n').split(','))
		#frequencyTable.append([j[0],j[1],int(j[2]),int(j[3]),j[4],int(j[5]),float(j[6]),float(j[7]),float(j[8])])

	print ('\nCreating language dictionaries ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()
	
	l.myclassifier(testing,frequencyTable,grams,wrongs,mytotal,myrecall,total)

	print ('\nPerforming classifications ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	for i in confusion:
		for j in confusion[i]:
			if i==j:
				confusion[i][j]=myrecall[j]
			else:
				confusion[i][j]=wrongs[i][j]	
	
	for g in grams:				
		for i in lang:
			numerator = 0
			denominator = 0										
			for j in confusion:
				if i==j: numerator += confusion[j][i][g]				
				denominator+= confusion[j][i][g]
			precision[g]+=(numerator/denominator/4) if denominator!=0 else 0
		for x in confusion:
			numerator = 0
			denominator = 0	
			for y in lang:
				if x==y: numerator += confusion[x][y][g]				
				denominator+= confusion[x][y][g]
			recall[g]+=(numerator/denominator/4) if denominator!=0 else 0

	print ('\nGenerating performance metrices - precission, recall and f-score ...  {}'.format(l.timer(mytime)))
	mytime = datetime.datetime.now()

	if os.path.isfile('result.txt'): os.remove('result.txt')
	r=open('result.txt','a+')

	print ('\nngram\t\tobservations\t    precision\t    recall\t    f-score')
	for g in grams:
		print ("{}\t\t{}\t\t{:10.4f}\t{:10.4f}\t{:10.4f}".format(g,total[g],precision[g],recall[g],2*((precision[g]*recall[g])/(precision[g]+recall[g]))))
		r.write(str(g)+","+str(total[g])+","+str(precision[g])+","+str(recall[g])+","+str(2*((precision[g]*recall[g])/(precision[g]+recall[g])))+str('\r\n'))
	r.close()
	
	print ('\nGenerating clasification performance results ...  {}'.format(l.timer(mytime)))

	print ('\nStarted:', started)
	ended = datetime.datetime.now()

	print ('End    :', ended)
	print ('Elapsed:{}'.format(l.timer(started)))

def main():
	os.system('clear') # on linux 
	choice=0; phraselength=0
	while choice!=0:
		print ('\n')
		print ('='*81).center(81)
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDTION').center(81)
		print ('-'*81).center(81)   
		try:			
			# maxngram = int(input('Insert one from (2,3,4,5) to set the ngram value:   '))
			phraselength = int(input('Insert one from (1,2,3,4,5) to set the test phrase length:   '))
			choice = int(input('Press 1 to classify [0 to exit] :   '))

		except ValueError:
			print ("\n\nError: Please enter 1 to continue searching or 0 to exit.")
			continue
		else:
			if choice==0:
				return
			else:
				if phraselength>5 or phraselength<1:
					print ('\n\nPlease check your entry on ngram value and or phrase length')
				else:
					classification(phraselength)
	
if __name__ == '__main__':
	main()