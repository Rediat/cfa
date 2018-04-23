import os
import sys
import re
import glob
import string
import datetime
import copy
import decimal
import operator

def savetofile(summary, started):

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
	
	if os.path.isfile('model2.txt'): os.remove('model2.txt')
	if os.path.isfile('metrix.txt'): os.remove('metrix.txt')
	
	pfile=open('model2.txt','a+')
	mfile=open('metrix.txt','a+')

	maximum = max(summary['mostfrequent'], key=summary['mostfrequent'].get)
	mysum = {'am':0,'gu':0,'ti':0,'ge':0}
	
	r = len(summary['model'])	
	for j,i in enumerate(summary['model']): #[lang[0],term[1],gram[2],freq[3]]
	
		mysum[i[0]] += i[3]

		print('\b'*40,end='')
		print('{} - {:0.2f}%'.format(datetime.datetime.now(),(j/r)*100),end='')
		#['lang'[0],'term'[1],'gram'[2],'freq'[3],'bytes'[4],'InFreq'[5],'OvFreq'[6],'percent'[7]]
		# print (i[0],i[1],i[2],i[3],sys.getsizeof(i[1]),(i[3]/summary['vocabulary'][i[0]]/summary['mostfrequent'][maximum])+1)#, (i[3]/summary['allngrams']/summary['mostfrequent'][maximum])+1, (mysum[i[0]]/summary['wordcount'][i[0]])]
		temp = [i[0],i[1],i[2],i[3],sys.getsizeof(i[1]),(i[3]/summary['vocabulary'][i[0]]/summary['mostfrequent'][maximum])+1, (i[3]/summary['allngrams']/summary['mostfrequent'][maximum])+1, (mysum[i[0]]/summary['wordcount'][i[0]])]		
		#['seq'[0],'term'[1],'freq'[2],'gram'[3],'bytes'[4],'lang'[5],'probability'[6],'InFreq'[7],'OvFreq'[8],'percent'[9]]
		pfile.write(str(temp[0])+","+str(temp[1])+","+str(temp[2])+","+str(temp[3])+","+str(temp[4])+","+str(temp[5])+","+str(temp[6])+","+str(temp[7])+str('\r\n'))
		# print ("{}\t{}\t{}\t{}\t{}\t{}\t{:10.4f}\t{:10.4f}\t{:10.4f}\t{:10.4f}".format(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8],temp[9]))
	pfile.close()
	rsummary = summary
	rsummary.pop('model')

	mfile.write(str(rsummary))
	mfile.close()
	print ('\n\nAll Ngrams:', summary['wordcount'],'\t\tAll Ngrams:',summary['allwords'],'\nVocabularies:',summary['vocabulary'],'\t\tAll Vocabulary:',summary['allngrams'])
	#,'\nMaximum:',summary['mostfrequent'],)
	# print ('Minimum:',summary['min'],'\tFreq:',summary['minfreq'],'\tTerm:',summary['minterm'],
	# print ('Maximum:',summary['max'],'\tFreq:',summary['maxfreq'],'\tTerm:',summary['maxterm'])
	
	print ('\nA total of {} Vocabularies are generated for all languages in model.txt file'.format(summary['allngrams']))
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
	print('\n{} - Started building a summary of the model for {} language'.format(datetime.datetime.now(),language[transit[0]]))
	# max,min,,100,0 ; minterm,maxterm='',''
	counter = 0 ; freq=0 ;uniques = 0
	lang =transit[0]
	uniques+=int(len(transit[1]))

	for l in transit[1].keys(): #new [lang[0],term[1],gram[2],freq[2]]		 
		temp = [lang,l,len(l),transit[1][l]]	#old [seq[0],term[1],freq[2],length[3],lang[4]]
		counter+=transit[1][l]

		if freq<temp[3]: freq=temp[3]		
		model.append(temp)	
	
	model.sort(key = lambda nn:nn[3], reverse = True)

	vocabulary[lang]= uniques 				#count of unique ngrams for a language
	mostfrequent[lang]=freq 			#most frequent of all ngrams in a language
	wordcount[lang] = counter 			#total ngram counts summing frequencies
	allwords = sum(wordcount.values())	#all ngrams sum of frequencies in all languages
	allngrams = sum(vocabulary.values())		#total count of all unique ngrams in all languages
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
	print('{} - Started building sorted frequency distribution for {} language'.format(datetime.datetime.now(),language[listed[0]]))
	wordslists = set(listed[1])
	frequencyTable = {}

	for i in wordslists:
		frequencyTable[i] = 0

	r = len(listed[1])

	print('{} - Matching {:,} vocabulary items to {:,} ngrams in {} language'.format(datetime.datetime.now(),r,len(listed[1]),language[listed[0]]))
	
	for j,items in enumerate(listed[1]):			
		if len(items)==0: continue
		i=0
		print('\b'*50,end='') ; print('{:0.2f}%'.format((j/r)*100),end='')
		frequencyTable[items]+=1
		
	# frequencyTable.sort(key = lambda nn:nn[1], reverse = True)
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
	for j in grams:
		for i in range(length):
			if(j+i==length):
				break
			if ind!=0:
				temp = [rawtext[1][i:j+i],j]
				if len(temp[0])<2 or len(temp[0].strip())==0:
					continue
			else:
				temp = rawtext[1][i:j+i]
				if len(temp)<2 or len(temp.strip())==0:
					continue
			textgrams.append(temp)
	return [rawtext[0],textgrams]

def regex(raw):
	lang=raw[0]
	rawtext = raw[1]
	#remove [፠፡።፣፤፥፦፧፨‚‛“”„‟›•※‼‽‾‿‹*()"?!.,|/@#$%^&<>0123456789]' []
	pattern = re.compile(u'[\u135D\u135E\u135F\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368\u201A\u201B\u201C\u201D\u201E\u201F\u203a\u2022\u203b\u203c\u203d\u203e\u203f\u2039*()"?!.\',|/@#$%^&<>0123456789]',re.UNICODE)
	sqbracket = re.compile(u'[/[/]]',re.UNICODE)

	cleaned = re.sub(pattern,' ',rawtext.strip())
	if lang=='am' or lang=='ti' or lang=='gu':				
		cleaned = re.sub(sqbracket,' ',cleaned.strip())
	else:	
		cleaned = re.sub(sqbracket,'',cleaned.strip())
	cleaned = re.sub(' +',' ',cleaned)
	return [lang,cleaned]

def regexs(rawtext,lang='am'):
	#remove [፠፡።፣፤፥፦፧፨‚‛“”„‟›•※‼‽‾‿‹*()"?!.,|/@#$%^&<>0123456789]' []
	pattern = re.compile(u'[\u135D\u135E\u135F\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368\u201A\u201B\u201C\u201D\u201E\u201F\u203a\u2022\u203b\u203c\u203d\u203e\u203f\u2039*()"?!.\',|/@#$%^&<>0123456789]',re.UNICODE)
	sqbracket = re.compile(u'[/[/]]',re.UNICODE)

	cleaned = re.sub(pattern,' ',rawtext.strip())
	if lang=='am' or lang=='ti' or lang=='gu':				
		cleaned = re.sub(sqbracket,' ',cleaned.strip())
	else:	
		cleaned = re.sub(sqbracket,'',cleaned.strip())
	cleaned = re.sub(' +',' ',cleaned)
	return cleaned	

def myclassifier(testing,frequencyDict,grams,wrongs,mytotals,myrecall,total,uniquengrams,totalngrams):
	
	for i in testing: #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		
		for g in grams:
			id=classify(frequencyDict,g,i[1],uniquengrams,totalngrams)
			if id[0]==1:continue
			checkCFA = 1 if i[0]==id[1] else 0
			checkNBC = 1 if i[0]==id[2] else 0

			if checkCFA==0:
				wrongs['CFA'][i[0]][id[1]][g]+=1
			
			if checkNBC==0:
				wrongs['NBC'][i[0]][id[2]][g]+=1
			
			mytotals['CFA'][i[0]][g]+=1
			mytotals['NBC'][i[0]][g]+=1
			total['CFA'][g]+=1
			total['NBC'][g]+=1
			myrecall['CFA'][i[0]][g]+=checkCFA
			myrecall['NBC'][i[0]][g]+=checkNBC

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

		if item[1]==grams: #[2,3,4,5]
			# frequencyDict {'am': {'ት ': {'freq': '99', 'ovFreq': '1.0000109646985438'}}, 'ge': {}, 'gu': {}, 'ti': {}}
			for items in lang: #{'የሳ', {'am': {fr1, 'ge': 1, 'gu': 1, 'ti': 1}
				try:					
					langCFA[items]+=float(frequencyDict[items][item[0]]['ovFreq'])
					ind=0					
					for i in nbc: #['የሳ', {'am': 1, 'ge': 1, 'gu': 1, 'ti': 1}]
						if i[0] == item[0]:
							i[1][items]+=int(frequencyDict[items][item[0]]['freq'])
				except KeyError:
					pass
	
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

def readsample(sample,phraselength=5):
	sampled=[]
	for i in sample:
		j = i.rstrip().split(',')
		temp = [j[0],j[1],j[2],j[3],j[4]] # [am,እውነት,1,4,82]
		if int(j[2])==int(phraselength): 
			sampled.append(temp)
	return sampled

def overallclassify(frequencyDict,sampled,grams,uniquengrams,totalngrams):

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
		for g in grams:
			if item[1]==g:
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

def overallmyclassifier(testing,frequencyDict,grams,overallwrongsCFA,overalltotal,overallrecallCFA,uniquengrams,overallwrongsNBC,overallrecallNBC,totalngrams):

	for i in testing:
		 #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		id=overallclassify(frequencyDict,i[1],grams,uniquengrams,totalngrams)
		checkCFA = 1 if i[0]==id[0] else 0			
		checkNBC = 1 if i[0]==id[1] else 0

		if checkCFA==0:
			overallwrongsCFA[i[0]][id[0]]+=1
		
		if checkNBC==0:
			overallwrongsNBC[i[0]][id[1]]+=1

		overalltotal[0]+=1;overalltotal[1]+=1
		overallrecallCFA[i[0]]+=checkCFA 
		overallrecallNBC[i[0]]+=checkNBC