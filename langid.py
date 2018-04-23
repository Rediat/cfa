import os
import sys
import re
import glob
import string
import datetime
import copy
import decimal
import operator

def savetofile(summary, started,ind=0):

	# model=model,					#[seq[0],term[1],freq[2],length[3],lang[4]]
	# allngrams=allngrams,			#total count of all unique ngrams in all languages
	# allwords=allwords,			#all ngrams sum of frequencies in all languages
	# vocabulary=vocabulary,					#count of unique ngrams for a language
	# freq=freq,					#most frequent ngram of a language
	# mostfrequent=mostfrequent,	#most frequent ngrams of each language
	# min=min,						#the shortest length of an ngram of all languages
	# max=max,						#the longest length of an ngram of all languages
	# minterm=minterm,				#the shortest length ngram of all languages
	# maxterm=maxterm,				#the longest length ngram of all languages
	# minfreq=minfreq,				#the frequency of shortest length ngram of all languages
	# maxfreq=maxfreq,				#the frequency of longest length ngram of all languages
	# wordcount=wordcount,			#total ngram counts with summing frequencies of each languages
	# uniques=uniques				#count of unique ngrams for a language
	
	if os.path.isfile('model.txt'): os.remove('model.txt')
	if os.path.isfile('metrix.txt'): os.remove('metrix.txt')
	
	pfile=open('model.txt','a+')
	mfile=open('metrix.txt','a+')

	maximum = max(summary['mostfrequent'], key=summary['mostfrequent'].get)
	mysum = {'am':0,'gu':0,'ti':0,'ge':0}

	counts = {} ; grams = (2,3,4,5) ; frequencies = {}
	lang = dict(am=0,ge=0,gu=0,ti=0)
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	
	if ind==2:
		counts = copy.deepcopy(lang)
		frequencies = copy.deepcopy(lang)
	else:
		for i in grams:
			counts[i] = copy.deepcopy(lang)
			frequencies[i] = copy.deepcopy(lang)

	# print (summary['model'])
	# return

	r = len(summary['model'])	
	for j,i in enumerate(summary['model']): #[lang[0],term[1],gram[2],freq[3]]
		mysum[i[0]] +=i[3]
		print('\b'*40,end='')
		print('\t{} - {:0.2f}%'.format(datetime.datetime.now(),(j/r)*100),end='')
		#['lang'[0],'term'[1],'gram'[2],'freq'[3],'bytes'[4],'InFreq'[5],'OvFreq'[6],'percent'[7]]
		temp = [i[0],i[1],i[2],i[3],sys.getsizeof(i[1]),(i[3]/summary['vocabulary'][i[0]]/summary['mostfrequent'][maximum])+1, (i[3]/summary['allngrams']/summary['mostfrequent'][maximum])+1, (mysum[i[0]]/summary['wordcount'][i[0]])]		
		if ind==2:
			counts[temp[0]]+=1 ; frequencies[temp[0]]+=temp[3]
		else:
			counts[int(temp[2])][temp[0]]+=1 ; frequencies[int(temp[2])][temp[0]]+=temp[3]
		pfile.write(str(temp[0])+","+str(temp[1])+","+str(temp[2])+","+str(temp[3])+","+str(temp[4])+","+str(temp[5])+","+str(temp[6])+","+str(temp[7])+str('\r\n'))
		
	pfile.close()
	rsummary = summary
	rsummary.pop('model')

	mfile.write(str(rsummary))
	mfile.close()

	print ('\n\nNgram Vocabularies : {}\t\tAll Vocabulary: {:,}\nFixed length Ngrams: {}\t\tAll Ngrams: {:,}'.format(summary['vocabulary'],summary['allngrams'],summary['wordcount'],summary['allwords']))
	print ('\nA total of {:,} Vocabularies are generated for all languages in model.txt file.'.format(summary['allngrams']))
	
	if ind==2:
		print('\n\t{}\n\t{:<15} {:<25}\n\t{}'.format('='*40,'Language','Word Vocabulary Details','-'*40))
		
		for i in lang:
			print('\t{:<15} {:,}'.format(language[i],counts[i]))
		print('{}{}'.format('\t','-'*40))

		print('\n\t{}\n\t{:<15} {:<25}\n\t{}'.format('='*40,'Language','Word Frequency Details','-'*40))
		for i in lang:
			print('\t{:<15} {:,}'.format(language[i],frequencies[i]))
		print('{}{}'.format('\t','-'*40))
	else:
		print ('\nGrams \t Ngram Vocabulary Details')
		for i in grams:
			print('{:<3}\t {}'.format(i,counts[i]))

		print ('\nGrams \t Ngram Frequency Details')
		for i in grams:
			print('{:<3}\t {}'.format(i,frequencies[i]))
	
	print ('\nStarted:', started)
	ended = datetime.datetime.now()
	elapsed = ended - started
	print ('End    :', ended)
	print ('Elapsed:', elapsed)

def timer(spent):
	running = datetime.datetime.now()
	return running-spent

def summerize(model,transit,mostfrequent,wordcount,vocabulary):
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	print('\n\t{} - Started building a summary of the model for {} language'.format(datetime.datetime.now(),language[transit[0]]))

	counter = 0 ; freq=0 ;uniques = 0
	lang =transit[0]
	uniques+=int(len(transit[1]))

	for l in transit[1].keys(): #new [lang[0],term[1],gram[2],freq[2]]		 
		temp = [lang,l,len(l),transit[1][l]]	#old [seq[0],term[1],freq[2],length[3],lang[4]]
		counter+=transit[1][l]

		if freq<temp[3]: freq=temp[3]		
		model.append(temp)	
	
	model.sort(key=lambda n:(n[0],n[3]),reverse = True) 

	vocabulary[lang]= uniques 				#count of unique ngrams for a language
	mostfrequent[lang]=freq 				#most frequent of all ngrams in a language
	wordcount[lang] = counter 				#total ngram counts summing frequencies
	allwords = sum(wordcount.values())		#all ngrams sum of frequencies in all languages
	allngrams = sum(vocabulary.values())	#total count of all unique ngrams in all languages
	summary = dict(
					model=model,				#[seq[0],term[1],freq[2],length[3],lang[4]]
					allngrams=allngrams,		#total count of all unique ngrams in all languages
					allwords=allwords,			#all ngrams sum of frequencies in all languages
					vocabulary=vocabulary,		#count of unique ngrams for a language
					mostfrequent=mostfrequent,	#most frequent ngrams of each language
					wordcount=wordcount,		#total ngram counts with summing frequencies of each languages
					uniques=uniques				#count of unique ngrams for a language
					)
	return summary

def wordgrams(listed):
	#ind to dicate considering frequency count
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	print('\t{} - Started building sorted frequency distribution for {} language'.format(datetime.datetime.now(),language[listed[0]]))
	
	lists = listed[1]

	wordslists = set(lists)			
	
	frequencyTable = {}

	for i in wordslists:
		frequencyTable[i] = 0

	r = len(lists)
	w = len(wordslists)

	print('\t{} - Matching {:,} vocabulary items to {:,} ngrams in {} language'.format(datetime.datetime.now(),w,len(listed[1]),language[listed[0]]))
	
	for j,items in enumerate(lists):			
		if len(items)==0: continue
		print('\b'*50,end='')
		print('\t{} - {:0.2f}%'.format(datetime.datetime.now(),(j/r)*100),end='')
		frequencyTable[items]+=1
	
	return [listed[0],frequencyTable]

def to_unicode(obj, encoding='utf8'):
	if isinstance(obj, str):
		if not isinstance(obj, str):
			obj = str(obj, encoding)
	return obj	

def ngram(rawtext,ind=0):
	grams = (2,3,4,5)
	textgrams=[]
	length = len(rawtext[1])+1
	
	for i in range(length):	
		for j in grams:			
			if(j+i==length):
				break
			if ind!=0:
				temp = [rawtext[1][i:j+i],j]
				if len(temp[0])<2 or len(temp[0].strip())==0 or len(temp[0])!=j:
					continue
			else:
				temp = rawtext[1][i:j+i]
				if len(temp)<2 or len(temp)!=j or len(temp.strip())==0:
					continue
			textgrams.append(temp)
	return [rawtext[0],textgrams]

def regex(raw):
	lang=raw[0] ; rawtext = raw[1]
	#remove [፠፡።፣፤፥፦፧፨‚‛“”„‟›•※‼‽‾‿‹*()"?!.,|/@#$%^&<>0123456789]' []
	pattern = re.compile(u'[\u135D\u135E\u135F\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368\u201A\u201B\u201C\u201D\u201E\u201F\u203a\u2022\u203b\u203c\u203d\u203e\u203f\u2039*()"?!.\',|/@#$%^&<>0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]',re.UNICODE)
	sqbracket = re.compile(r'[\[\]]',re.UNICODE)

	cleaned = re.sub(pattern,' ',rawtext.strip())
	if lang=='am' or lang=='ti' or lang=='gu':				
		cleaned = re.sub(sqbracket,' ',cleaned.strip())
	elif lang=='ge':	
		cleaned = re.sub(sqbracket,'',cleaned.strip())

	cleaned = re.sub(' +',' ',cleaned)
	return [lang,cleaned]

def regexs(rawtext,lang='am'):
	#remove [፠፡።፣፤፥፦፧፨‚‛“”„‟›•※‼‽‾‿‹*()"?!.,|/@#$%^&<>0123456789]' []
	pattern = re.compile(u'[\u135D\u135E\u135F\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368\u201A\u201B\u201C\u201D\u201E\u201F\u203a\u2022\u203b\u203c\u203d\u203e\u203f\u2039*()"?!.\',|/@#$%^&<>0123456789]',re.UNICODE)
	sqbracket = re.compile(r'[\[\]]',re.UNICODE)

	cleaned = re.sub(pattern,' ',rawtext.strip())
	if lang=='am' or lang=='ti' or lang=='gu':				
		cleaned = re.sub(sqbracket,' ',cleaned.strip())
	elif lang=='ge':	
		cleaned = re.sub(sqbracket,'',cleaned.strip())
	cleaned = re.sub(' +',' ',cleaned)
	return cleaned	

def myclassifier(testing,frequencyDict,grams,wrongs,totaltests,myrecall,total,uniquengrams,totalngrams):
	
	for i in testing: #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]

		for g in grams:
			id=classify(frequencyDict,g,i[1],uniquengrams,totalngrams)
			totaltests['CFA'][g]+=1 ; totaltests['NBC'][g]+=1
			if id[0]==1: continue

			check = dict(CFA=0,NBC=0)
			check['CFA'] = 1 if i[0]==id[1] else 0
			check['NBC'] = 1 if i[0]==id[2] else 0

			if check['CFA']==0:
				wrongs['CFA'][i[0]][id[1]][g]+=1
			
			if check['NBC']==0:
				wrongs['NBC'][i[0]][id[2]][g]+=1

			total['CFA'][g]+=1 ; total['NBC'][g]+=1
			myrecall['CFA'][i[0]][g]+=check['CFA']
			myrecall['NBC'][i[0]][g]+=check['NBC']

def wrongclassifications(wrongs,wrongid,grams):
	for i in wrongs:
		for j in wrongs[i]:
			for g in grams:
				if wrongs[i][j][g]!=0:
					wrongid.append([i,j,g,wrongs[i][j][g]])
	return wrongid

def classify(frequencyDict,grams,sampled,uniquengrams,totalngrams):
	
	lang = ['am','ge','gu','ti']
	langCFA = dict(am=0,ge=0,gu=0,ti=0)
	langNBC = copy.deepcopy(langCFA)
	prior =  copy.deepcopy(langCFA)	
	alluniquengrams = sum(uniquengrams.values())
	nbc=[]

	ind=1 #to indicate the overflow of grams from max length of the ngram

	langCFA = langCFA.fromkeys(langCFA,0) #set all values of lang to 0
	langNBC = langNBC.fromkeys(langNBC,1)
	
	for j in sampled:
		if j[1]==grams:
			nbc.append([j[0],copy.deepcopy(langNBC)])
	
	for item in sampled: #[['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]
		
		if item[1]!=grams: continue#[2,3,4,5]
			# frequencyDict {'am': {'ት ': {'freq': '99', 'ovFreq': '1.0000109646985438'}}, 'ge': {}, 'gu': {}, 'ti': {}}
		for items in lang: #{'የሳ', {'am': {fr1, 'ge': 1, 'gu': 1, 'ti': 1}
			try:					
				langCFA[items]+=float(frequencyDict[items][item[0]]['ovFreq'])				
				for i in nbc: #['የሳ', {'am': 1, 'ge': 1, 'gu': 1, 'ti': 1}]
					if i[0] == item[0]:
						i[1][items]+=int(frequencyDict[items][item[0]]['freq'])
				ind=0
			except KeyError:
				pass
	
	if ind==0:
		for i in langNBC:
			for j in nbc:
				# j[1][i] += 1
				j[1][i]/=(totalngrams[i]+alluniquengrams+1)			
			prior[i]=uniquengrams[i]/alluniquengrams if alluniquengrams!=0 else 0

		for i in langNBC:							
			for j in nbc:
				langNBC[i] *= decimal.Decimal(j[1][i])

		for j in langNBC:
			langNBC[j] *= decimal.Decimal(prior[j])

		maximumCFA = max(langCFA, key=langCFA.get)
		maximumNBC = max(langNBC, key=langNBC.get)

		return [ind,maximumCFA,maximumNBC]
	else:
		return [ind]

def readsample(sample,phraselength=5):
	sampled=[]
	for i in sample:
		j = i.rstrip().split(',')
		temp = [j[0],j[1],j[2],j[3],j[4]] # [am,እውነት,1,4,82]
		if int(j[2])==int(phraselength): 
			sampled.append(temp)
	return sampled

def overallclassify(frequencyDict,sampled,uniquengrams,totalngrams):

	lang = ['am','ge','gu','ti']
	langCFA = dict(am=0,ge=0,gu=0,ti=0)
	langNBC = copy.deepcopy(langCFA)
	prior =  copy.deepcopy(langCFA)	
	alluniquengrams = sum(uniquengrams.values())
	#alltotalngrams = sum(totalngrams.values())
	nbc=[]
	
	langCFA = langCFA.fromkeys(langCFA,0) #set all values of lang to 0
	langNBC = langNBC.fromkeys(langNBC,1)

	for j in sampled:
		nbc.append([j[0],copy.deepcopy(langNBC)])
	
	for item in sampled: #['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		# for g in grams:
		# 	if item[1]==g:
		for items in lang: #[am,ት ,2,2,78,1.0043572984749456,1.0009775171065494,0.012987012987012988]
			try:
				langCFA[items]+=float(frequencyDict[items][item[0]]['ovFreq'])					
				for i in nbc:
					if i[0] == item[0]:	
						i[1][items]+=int(frequencyDict[items][item[0]]['freq'])
			except KeyError:
				pass

	for i in langNBC:
		for j in nbc:
			# j[1][i] += 1
			j[1][i]/=(totalngrams[i]+alluniquengrams+1)			
		prior[i]= uniquengrams[i]/alluniquengrams if alluniquengrams!=0 else 0

	for i in langNBC:							
		for j in nbc:
			langNBC[i] *= decimal.Decimal(j[1][i])

	for j in langNBC:
		langNBC[j] *= decimal.Decimal(prior[j])

	maximumCFA = max(langCFA, key=langCFA.get)
	maximumNBC = max(langNBC, key=langNBC.get)

	return [maximumCFA,maximumNBC]

def overallmyclassifier(testing,frequencyDict,overallwrongs,overalltotal,overallrecall,uniquengrams,totalngrams):

	for i in testing:
		 #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		id=overallclassify(frequencyDict,i[1],uniquengrams,totalngrams)
		check = dict(CFA=0,NBC=0)
		check['CFA'] = 1 if i[0]==id[0] else 0			
		check['NBC'] = 1 if i[0]==id[1] else 0

		if check['CFA']==0:
			overallwrongs['CFA'][i[0]][id[0]]+=1
		
		if check['NBC']==0:
			overallwrongs['NBC'][i[0]][id[1]]+=1

		overalltotal['CFA']+=1;overalltotal['NBC']+=1
		overallrecall['CFA'][i[0]]+=check['CFA'] 
		overallrecall['NBC'][i[0]]+=check['NBC']