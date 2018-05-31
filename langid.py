import os ; import sys ; import re ; import glob ; import string ; import datetime ; import copy ; import decimal ; import operator

def savetofile(summary,started,mod,maxg=5,ct=1):

	# model=model,						#[seq[0],term[1],freq[2],length[3],lang[4]]
	# allngrams=allngrams,				#total count of all unique ngrams in all languages
	# allwords=allwords,				#all ngrams sum of frequencies in all languages
	# vocabulary=vocabulary,			#count of unique ngrams of all languages
	# mostfrequent=mostfrequent,		#most frequent ngrams of each language
	# wordcount=wordcount,				#total ngram counts with summing frequencies of each languages
	# uniques=uniques,					#count of unique ngrams for a language
	# modeltype=transit[2],				#indicate the model type
	# percent=transit[3],				#percentage to top frequent words selected for modelling
	# langvocabulary=langvocabulary 	#count of unique ngrams for each language

	path='models/'+str(ct)+'/'
	myfile=summary['modeltype']+'.txt'
	if mod=='wr':
		if os.path.isfile(os.path.join(path, myfile)): os.remove(os.path.join(path, myfile))
		wfile=open(os.path.join(path, myfile),'a+')
		
	else:	
		# if os.path.isfile('model.txt'): os.remove('model.txt')
		if os.path.isfile(os.path.join(path, myfile)): os.remove(os.path.join(path, myfile))
		pfile=open(os.path.join(path, myfile),'a+')
	
	if os.path.isfile('metrix.txt'): os.remove('metrix.txt')
	mfile=open('metrix.txt','a+')

	maximum = max(summary['mostfrequent'], key=summary['mostfrequent'].get)
	mysum = {'am':0,'gu':0,'ti':0,'ge':0}

	counts = {} ; frequencies = {}
	# grams = (2,3,4,5) 
	grams = [x for x in range(2,6)] if maxg==5 else [x for x in range(2,maxg+1)]
	lang = dict(am=0,ge=0,gu=0,ti=0)
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	
	if  mod=='wr':
		counts = copy.deepcopy(lang)
		frequencies = copy.deepcopy(lang)
		wordlenfreq = dict(am={},ge={},gu={},ti={})
		checklen=dict(am=[],ge=[],gu=[],ti=[])
		wordbyte = dict(am={},ge={},gu={},ti={})

	else:
		for i in grams:
			counts[i] = copy.deepcopy(lang)
			frequencies[i] = copy.deepcopy(lang)

	r = len(summary['model'])
	
	for j,i in enumerate(summary['model']): #[lang[0],term[1],gram[2],freq[3]]
		mysum[i[0]] +=i[3]
		print('\b'*40,end='')
		print('\t{} - {:0.2f}%'.format(datetime.datetime.now(),((j+1)/r)*100),end='')
		#['lang'[0],'term'[1],'gram'[2],'freq'[3],'bytes'[4],'OvFreq'[5],'percent'[6]
		# temp = [i[0],i[1],i[2],i[3],sys.getsizeof(i[1]),(i[3]/summary['vocabulary'][i[0]]/summary['mostfrequent'][maximum])+1, (i[3]/summary['allngrams']/summary['mostfrequent'][maximum])+1, (mysum[i[0]]/summary['wordcount'][i[0]]),(i[3]/summary['vocabulary'][i[0]])+1]		
		temp = [i[0],i[1],i[2],i[3],sys.getsizeof(i[1]),(i[3]/summary['allngrams']/summary['mostfrequent'][maximum])+1, (mysum[i[0]]/summary['wordcount'][i[0]])]				
		if mod=='wr':
			if temp[2] not in checklen[i[0]]: checklen[i[0]].append(temp[2]) ; wordlenfreq[i[0]][temp[2]]=0 ; wordbyte[i[0]][temp[2]]=0
			counts[temp[0]]+=1 ; frequencies[temp[0]]+=temp[3]
			wordlenfreq[i[0]][temp[2]]+=1 ;  wordbyte[i[0]][temp[2]]=temp[4]
			wfile.write(str(temp[0])+","+str(temp[1])+","+str(temp[2])+","+str(temp[3])+","+str(temp[4])+","+str(temp[6])+str('\r\n'))
		else:
			# print(counts,temp[2],temp[0],temp[3],maxg, grams)
			counts[int(temp[2])][temp[0]]+=1 ; frequencies[int(temp[2])][temp[0]]+=int(temp[3])
			pfile.write(str(temp[0])+","+str(temp[1])+","+str(temp[2])+","+str(temp[3])+","+str(temp[4])+","+str(temp[5])+","+str(temp[6])+","+str(summary['percent'])+str('\r\n'))
		
	if mod=='wr':
		wfile.close()
	else:
		pfile.close()
	
	rsummary = summary
	rsummary.pop('model')

	mfile.write(str(rsummary))
	mfile.close()

	print ('\n\nNgram Vocabularies : {}\t\tAll Vocabulary: {:,}\nFixed length Ngrams: {}\t\tAll Ngrams: {:,}'.format(summary['vocabulary'],summary['allngrams'],summary['wordcount'],summary['allwords']))
	print ('\nA total of {:,} Vocabularies are generated for all languages in models/{}/{} file.'.format(summary['allngrams'],ct,myfile))
	
	if mod=='wr':
		print('\n\t{}\n\t{:<15} {:<25}\n\t{}'.format('='*40,'Language','Word Vocabulary Details','-'*40))
		
		for i in lang:
			print('\t{:<15} {:,}'.format(language[i],counts[i]))
		print('{}{}'.format('\t','-'*40))

		print('\n\t{}\n\t{:<15} {:<25}\n\t{}'.format('='*40,'Language','Word Frequency Details','-'*40))
		for i in lang:
			print('\t{:<15} {:,}'.format(language[i],frequencies[i]))
		print('{}{}'.format('\t','-'*40))

		print('\n\t{}\n\t{:10} {:10} \t {:10} \t {:10} \t {:10}\n\t{}'.format('='*70,'Language','Characters','Byte','Frequency','Percent','-'*70))
		for i in lang:
			for j in wordlenfreq[i]:
				print('\t{:10} {:10,} \t {:10,} \t {:10,} \t{:10.2f}%'.format(language[i],j,wordbyte[i][j],wordlenfreq[i][j],(wordlenfreq[i][j]/sum(wordlenfreq[i].values()))*100))
		print('{}{}'.format('\t','-'*70))
	else:
		print ('\nGrams \t Ngram Vocabulary Details')
		for i in grams:
			print('{:<3}\t {}'.format(i,counts[i]))

		print ('\nGrams \t Ngram Frequency Details')
		for i in grams:
			print('{:<3}\t {}'.format(i,frequencies[i]))

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

	vocabulary[lang] = uniques				#count of unique ngrams for each language
	mostfrequent[lang]=freq 					#most frequent of all ngrams in a language
	wordcount[lang] = counter 					#total ngram counts summing frequencies
	allwords = sum(wordcount.values())			#all ngrams sum of frequencies in all languages
	allngrams = sum(vocabulary.values())	#total count of all unique ngrams in all languages
	summary = dict(
					model=model,					#[seq[0],term[1],freq[2],length[3],lang[4]]
					allngrams=allngrams,			#total count of all unique ngrams in all languages
					allwords=allwords,				#all ngrams sum of frequencies in all languages
					vocabulary=vocabulary,			#count of unique ngrams of all languages
					mostfrequent=mostfrequent,		#most frequent ngrams of each language
					wordcount=wordcount,			#total ngram counts with summing frequencies of each languages
					uniques=uniques,				#count of unique ngrams for a language
					modeltype=transit[2],			#indicate the model type
					percent=transit[3]				#percentage to top frequent words selected for modelling
					)
	return summary

def wordgrams(listed):
	#ind to dicate considering frequency count
	language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	print('\t{} - Started building sorted frequency distribution for {} language'.format(datetime.datetime.now(),language[listed[0]]))
	percent = listed[3] if len(listed)==4 else 1
	lists = listed[1]

	wordslists = set(lists)			
	
	frequencyTable = {}

	rejected = 0 #to exclude 1 character words
	for i in wordslists:
		# if len(i)<2: rejected+=1 ;continue
		frequencyTable[i] = 0

	r = len(lists)
	w = len(wordslists) - rejected

	print('\t{} - Matching {:,} vocabulary items to {:,} ngrams in {} language'.format(datetime.datetime.now(),w,len(listed[1]),language[listed[0]]))
	
	for j,items in enumerate(lists):			
		# if len(items)==0 or len(items)==1: continue
		if len(items)==0: continue
		print('\b'*50,end='')
		print('\t{} - {:0.2f}%'.format(datetime.datetime.now(),((j+1)/r)*100),end='')
		frequencyTable[items]+=1
	
	return [listed[0],frequencyTable,listed[2],percent]

def to_unicode(obj, encoding='utf8'):
	if isinstance(obj, str):
		if not isinstance(obj, str):
			obj = str(obj, encoding)
	return obj	

def ngram(rawtext,ind=0,pad=0,infinity=0):
	
	grams = [x for x in range(2,6)] if infinity==0 else [x for x in range(2,len(rawtext[1])+1)]
	textgrams=[] ; lang = rawtext[0]
	
	for j in grams:
		padding = '_'*(j-1)
		text = rawtext[1] if pad==0 else (padding+rawtext[1]+padding)
		length = len(text)+1
		for i in range(length):						
			if(j+i==length): break					
			if ind!=0:
				temp = [text[i:j+i],j]
				if len(temp[0])<2 or len(temp[0].strip())==0 or len(temp[0])!=j:
					continue
			else:
				temp = text[i:j+i]
				if len(temp)<2 or len(temp)!=j or len(temp.strip())==0:
					continue
			textgrams.append(temp)
	return [lang,textgrams]

def regex(raw):
	lang=raw[0] ; rawtext = raw[1]
	#remove [፠፡።፣፤፥፦፧፨‚‛“”„‟›•※‼‽‾‿‹*()"?!.,|/@#$%^&<>0123456789]' [] ‘– — ― ‗ ‘ ’ ‚ ‛ “ ” „ † ‡ • … ‰ ′ ″ ‹ › ‼ ‾ ⁄ ⁊ 
	pattern = re.compile(u'[\u2013\u2014\u2015\u2017\u2018\u2019\u201A\u201B\u201C\u201D\u201E\u2020\u2021\u2022\u2026\u2030\u2032\u2033\u2039\u203A\u203C\u203E\u2044\u204A\u135D\u135E\u135F\u1360\u1361\u1362\u1363\u1364\u1365\u1366\u1367\u1368\u201A\u201B\u201C\u201D\u201E\u201F\u203a\u2022\u203b\u203c\u203d\u203e\u203f\u2039*()"?!.\',-|/@#$%^&<>0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]',re.UNICODE)
	
	sqbracket = re.compile(r'[\[\]]',re.UNICODE)

	cleaned = re.sub(pattern,' ',rawtext.strip())
	if lang=='am' or lang=='ti' or lang=='gu':				
		cleaned = re.sub(sqbracket,' ',cleaned.strip())
	elif lang=='ge':	
		cleaned = re.sub(sqbracket,'',cleaned.strip())

	cleaned = re.sub(' +',' ',cleaned)
	return [lang,cleaned]

def myclassifier(testing,frequencyDict,grams,wrongs,totaltests,myrecall,total,uniquengrams,totalngrams,phrases,vocabulary):
	
	for j, i in enumerate(testing): #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		
		print('\b'*40,end='')
		print('{:0.2f}%'.format(((j+1)/phrases)*100),end='')
		
		for g in grams:
			
			id=classify(frequencyDict,g,i[1],uniquengrams,totalngrams,vocabulary)
			totaltests['CFA'][g]+=1 ; totaltests['NBC'][g]+=1
			# if id[0]==1: continue

			check = dict(CFA=0,NBC=0)
			check['CFA'] = 1 if i[0]==id[0] else 0
			check['NBC'] = 1 if i[0]==id[1] else 0

			if check['CFA']==0:
				wrongs['CFA'][i[0]][id[0]][g]+=1
			
			if check['NBC']==0:
				wrongs['NBC'][i[0]][id[1]][g]+=1

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

def classify(frequencyDict,grams,sampled,uniquengrams,totalngrams,vocabulary):
	
	lang = ['am','ge','gu','ti']
	langCFA = dict(am=0,ge=0,gu=0,ti=0)
	langNBC = copy.deepcopy(langCFA)
	prior =  copy.deepcopy(langCFA)	
	alluniquengrams = sum(uniquengrams.values())
	nbc=[] #; ind=1 #to indicate the overflow of grams from max length of the ngram

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
				# frequencyDict.get('am',{}).get('ት',{}).get('freq',-1)
				# langCFA[items]+=decimal.Decimal(0 if frequencyDict.get(items,{}).get(item[0],{}).get('ovFreq',-1)==-1 else frequencyDict[items][item[0]]['ovFreq'])				
				langCFA[items]+=decimal.Decimal(frequencyDict[items][item[0]]['ovFreq'])							
				for i in nbc: #['የሳ', {'am': 1, 'ge': 1, 'gu': 1, 'ti': 1}]
					if i[0] == item[0]:
						# i[1][items]+=int(0 if frequencyDict.get(items,{}).get(item[0],{}).get('freq',-1)==-1 else frequencyDict[items][item[0]]['freq'])
						i[1][items]+=int(frequencyDict[items][item[0]]['freq'])
				#ind=0
			except KeyError: pass
	
	# if ind==0:
	for i in langNBC:
		for j in nbc:
			j[1][i]/=(totalngrams[i]+vocabulary)			
		prior[i]=uniquengrams[i]/alluniquengrams if alluniquengrams!=0 else 0

	for i in langNBC:							
		for j in nbc:
			langNBC[i] *= decimal.Decimal(j[1][i])

	for j in langNBC:
		langNBC[j] *= decimal.Decimal(prior[j])

	maximumCFA = max(langCFA, key=langCFA.get)
	maximumNBC = max(langNBC, key=langNBC.get)

	# return [ind,maximumCFA,maximumNBC]
	return [maximumCFA,maximumNBC]
	# else:
	# 	return [ind]

def readsample(sample,phraselength=5, wordbased=0, location=0, infinity=0):
	sampled=[] ; averagebyte=0; n=0 ; characters=0
	
	#Breaks the text line in to a list and select only qualifying rows
	#Counts the number of testing phrases qualified and their average bytes
	for i in sample:
		j = i.rstrip().split(',')
		temps = [j[0],j[1],j[2],j[3],j[4]] # [am,እውነት,1,4,82]
		if int(j[2])==int(phraselength): 
			sampled.append(temps)
			averagebyte+=int(temps[4]) 
			characters+= int(temps[3])
			n+=1
	
	temp=[] ; phrases = 0 ; testing=[]

	# Breaks the testing phrases to a matiching type n-gram with the model
	for i in sampled: # [am,እውነት,1,4,82]
		if wordbased==0: # convert it to [['am', [['የዳ', 2], ['ዳዊ', 2], ['ዊት', 2], ['የዳዊ', 3], ['ዳዊት', 3], ['የዳዊት', 4]]]]
			testing.append(ngram(regex(i),1))	
			phrases+=1
		else:
			temp = regex(i)[1].split()
			wordlist = []
			for j in temp:
				if location==0:
					wordlist.extend(ngram([i[0],j],1,location,infinity)[1])
				else:
					wordlist.extend(ngram([i[0],j],1,location,infinity)[1])
			testing.append([i[0],wordlist])
			phrases+=1

	return [testing,averagebyte/n,characters/n,phrases]

def readmodel(path,mod,frequencyDict,totalngrams,uniquengrams):
	try:
		filename=mod+'.txt' ; vocabulary = set()
		f=open(os.path.join(path, filename),'r')
		model = f.readlines() ; n=0
		norepeat = set() ; 	r = len(model) ; maxg = 5
		for j, temp in enumerate(model): # [ti[0], እ[1],2[3],2570[3],78[4],1.0000010265081765[5],0.0066404493801385965[6]]
			print('\b'*50,end='')
			print('Reading relevant language models: {:0.2f}%'.format(((j+1)/r)*100),end='')
			temps = temp.rstrip('\n').split(',')
			totalngrams[temps[0]]+=int(temps[3])
			frequencyDict[temps[0]][temps[1]]=dict(gram=temps[2],freq=temps[3],ovFreq=decimal.Decimal(temps[5]))
			maxg = int(temps[2]) if maxg < int(temps[2]) else maxg
			vocabulary.add(temps[1]) ; n+=1
			if temps[1] not in norepeat:
				uniquengrams[temps[0]]+=1
				norepeat.add(temps[1])
		f.close()
		return [frequencyDict,uniquengrams,totalngrams,maxg,len(vocabulary),n]
	except ValueError:
		print ('\n\n Readmodel - Can not read the model file')

def overallclassify(frequencyDict,sampled,uniquengrams,totalngrams,vocabulary):

	lang = ['am','ge','gu','ti']
	langCFA = dict(am=0,ge=0,gu=0,ti=0)
	langNBC = copy.deepcopy(langCFA)
	prior =  copy.deepcopy(langCFA)	
	alluniquengrams = sum(uniquengrams.values())
	nbc=[] #; ind=1
	
	langCFA = langCFA.fromkeys(langCFA,0) #set all values of lang to 0
	langNBC = langNBC.fromkeys(langNBC,1)

	for j in sampled:
		nbc.append([j[0],copy.deepcopy(langNBC)])
	
	for item in sampled: #['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		
		for items in lang: #[am,ት ,2,2,78,1.0043572984749456,1.0009775171065494,0.012987012987012988]
			try:
				langCFA[items]+=decimal.Decimal(frequencyDict[items][item[0]]['ovFreq'])					
				for i in nbc:
					if i[0] == item[0]:	
						i[1][items]+=int(frequencyDict[items][item[0]]['freq'])
			
			except KeyError: pass
	
	for i in langNBC:
		for j in nbc:
			j[1][i]/=(totalngrams[i]+vocabulary)			
		prior[i]= uniquengrams[i]/alluniquengrams if alluniquengrams!=0 else 0

	for i in langNBC:							
		for j in nbc:
			langNBC[i] *= decimal.Decimal(j[1][i])

	for j in langNBC:
		langNBC[j] *= decimal.Decimal(prior[j])

	maximumCFA = max(langCFA, key=langCFA.get)
	maximumNBC = max(langNBC, key=langNBC.get)

	return [maximumCFA,maximumNBC]

def overallmyclassifier(testing,frequencyDict,overallwrongs,overalltotal,overallrecall,uniquengrams,totalngrams,phrases,vocabulary):

	for j, i in enumerate(testing): #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		
		print('\b'*40,end='')
		print('{:0.2f}%'.format(((j+1)/phrases)*100),end='')

		id=overallclassify(frequencyDict,i[1],uniquengrams,totalngrams,vocabulary)
		
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