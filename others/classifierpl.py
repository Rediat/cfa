import os
import sys
import re
import glob
import string
import datetime
import copy
import modeler as md

#Todo
	#Remove repetition of grams befor running the classifier[with and with out repetition in test]
	#Consider multilingual testing samples
	#Build classifier for Naive Bayes and Frequency Rank
	#Create a file that execues modeler sampler and classifier one after the other execute.py
	#modularize classifier.py in to functions
	#measure performace based on number of words in sample query

def classification():

	#*************************** START Reading Files ************************************

	started = datetime.datetime.now()
	phraselength = 5
	# fulltable=[]
	# wrongtable = []
	f=open('model.txt','r', encoding = 'utf8' )
	#m=open('metrix.txt','r', encoding = 'utf8' )
	s=open('sample.txt','r', encoding = 'utf8' )

	print ('\nOpening relevant files ...  {}'.format(md.timer(started)))
	mytime = datetime.datetime.now()
	
	model = f.readlines()
	#matrix = m.read()
	print ('\nReading language models ...  {}'.format(md.timer(mytime)))
	mytime = datetime.datetime.now()
	
	sample = s.readlines()
	f.close()
	s.close()
	#m.close()
	#*************************** END Reading Files ***************************************
	print ('\nReading test strings ...  {}'.format(md.timer(mytime)))
	mytime = datetime.datetime.now()

	wrongid = [] #wrongly classified identified

	sampled=[]
	for i in sample:
		j = i.rstrip().split(',')
		temp = [j[0],j[1],j[2]]
		#temp = [am,እውነት,1]
		sampled.append(temp)

	grams = (2,3,4,5)

	totals = {}
	total = dict(am={},ti={},gu={},ge={},no={})

	for i in total:
		for j in grams:
			totals[j]=0
		total[i]=copy.deepcopy(totals)
	totals = {}

	wrongs={}
	for i in total:
		wrongs[i]={}
		for j in range(1,phraselength+1):
			wrongs[i][j]=copy.deepcopy(total)

	myprecsion = copy.deepcopy(wrongs)
	precsion = copy.deepcopy(wrongs)
	mytotal = copy.deepcopy(wrongs)

	testing=[]
	for i in sampled:		
		testing.append(md.ngram(md.regex(i),1))	
	
	frequencyTable=[]
	for temp in model:
		frequencyTable.append(temp.rstrip('\n').split(','))

	print ('\nCreating language dictionaries ...  {}'.format(md.timer(mytime)))
	mytime = datetime.datetime.now()
	#print ('testing',testing[0])
	myclassifier(testing,frequencyTable,grams,wrongs,mytotal,myprecsion,phraselength)

	if os.path.isfile('result.txt'): os.remove('result.txt')
	r=open('result.txt','a+')

	print ('\nPerforming classifications and measuring precisions ...  {}'.format(md.timer(mytime)))
	mytime = datetime.datetime.now()

	print ("\n{}\t{}\t{}\t\t{}\t{}\t\t{}".format('anotation', 'phraselength','ngram','observations','correct','precision'))
	for x in total:
		for z in range(1,phraselength+1):
			for i in mytotal:			
				for j in grams:
					if mytotal[x][z][i][j]==0: continue
					if mytotal[x][z][i][j]!=0:
						precsion[x][z][i][j] = myprecsion[x][z][i][j]/mytotal[x][z][i][j]
					print ("{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(i,z,j,mytotal[x][z][i][j],myprecsion[x][z][i][j],precsion[x][z][i][j]))
					r.write(str(i)+","+str(z)+","+str(j)+","+str(mytotal[x][z][i][j])+","+str(myprecsion[x][z][i][j])+","+str(precsion[x][z][i][j])+str('\r\n'))
	r.close()
	
	print ('\nGenerating clasification performance results ...  {}'.format(md.timer(mytime)))

	print ('\nWrong classification:')
	widentified = wrongclassifications(total,wrongs,wrongid,grams,phraselength)
	print ("\nanotated\tphraselength\tclassified\tngram\tcounts")
	for i in widentified:
		print('{}\t\t{}\t\t{}\t\t{}\t{}'.format(i[0],i[1],i[2],i[3],i[4]))

	print ('\nStarted:', started)
	ended = datetime.datetime.now()

	print ('End    :', ended)
	print ('Elapsed:{}'.format(md.timer(started)))

def myclassifier(testing,frequencyTable,grams,wrongs,mytotal,myprecsion,phraselength):
	# q=0
	for i in testing:
		# q+=1
		# if q==10: break	
		for z in range(1,phraselength+1):	
			for j in grams:
				#id=[ind,maximum,lang]			
				id=classify(frequencyTable,j,i[1],z)
				if id[0]==1:continue
				check = 1 if i[0]==id[1] else 0
				#print ("{}\t{}\t{}\t{}\t{}".format(j,i[0],id[1],check,id[2]))			
				#r.write(str(j)+","+str(i[0])+","+str(id[1])+","+str(check)+","+str(id[2])+str('\r\n'))
				if check==0:
					wrongs [i[0]][z][id[1]][j]+=1

				mytotal[i[0]][z][id[1]][j]+=1
				myprecsion[i[0]][z][id[1]][j]+=check

def wrongclassifications(total,wrongs,wrongid,grams,phraselength):
	for x in total:
		for z in range(1,phraselength+1):
			for i in wrongs:
				for j in grams:
					if wrongs[x][z][i][j]!=0:
						wrongid.append([x,z,i,j,wrongs[x][z][i][j]])
	return wrongid

def classify(frequencyTable,grams,sampled,z):
	lang = dict(am=0,ti=0,gu=0,ge=0,no=0)
	ind=1 #to indicate the overflow of grams from max length of the ngram
	lang = lang.fromkeys(lang,0) #set all values of lang to 0
	norepeat = set() 
	for item in sampled:
		if (md.to_unicode(item[0]),z) in norepeat: continue
		if item[1]==grams:
			for items in frequencyTable:
				if md.to_unicode(items[1])==md.to_unicode(item[0]) and grams==item[1] and item[2]==z:
					lang[items[4]]+=float(items[7])
					ind=0
					norepeat.add((item[0],z))

	minimum = min(lang, key=lang.get)
	maximum = max(lang, key=lang.get)
	if minimum==maximum:
		return [ind,'no',lang]
	else:
		return [ind,maximum,lang]

def main():
	classification()
	
if __name__ == '__main__':
	main()