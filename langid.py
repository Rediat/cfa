import os
import sys
import re
import glob
import string
import datetime

def savetofile(summary, started):

	#model = [seq,term,freq,length,lang]
	#summary = dict(
	#				model=model,
	# 				maximum=maximum,
	# 				min=min,max=max,
	# 				minterm=minterm,
	# 				maxterm=maxterm,
	# 				minfreq=minfreq,
	# 				maxfreq=maxfreq,
	# 				wordcount=wordcount,
	# 				uniques=uniques)
	
	if os.path.isfile('model.txt'): os.remove('model.txt')
	if os.path.isfile('metrix.txt'): os.remove('metrix.txt')
	
	pfile=open('model.txt','a+')
	mfile=open('metrix.txt','a+')

	maximum = max(summary['mostfrequent'], key=summary['mostfrequent'].get)
	mysum = {'am':0,'gu':0,'ti':0,'ge':0}
	for i in summary['model']:
		mysum[i[4]] +=i[2]
		temp = [i[0],i[1],i[2],i[3],i[4],sys.getsizeof(i[1]),(i[2]/summary['wordcount'][i[4]]),(i[2]/summary['grams'][i[4]]/summary['mostfrequent'][maximum]), (i[2]/summary['allngrams']/summary['mostfrequent'][maximum]), (mysum[i[4]]/summary['wordcount'][i[4]])]		
		#['seq'[0],'term'[1],'freq'[2],'gram'[3],'bytes'[4],'lang'[5],'prob'[6],'InFreq'[7],'OvFreq'[8],'percent'[9]]
		pfile.write(str(temp[0])+","+str(temp[1])+","+str(temp[2])+","+str(temp[3])+","+str(temp[4])+","+str(temp[5])+","+str(temp[6])+","+str(temp[7])+","+str(temp[8])+str('\r\n'))
		print ("{}\t{}\t{}\t{}\t{}\t{}\t{:10.4f}\t{:10.4f}\t{:10.4f}\t{:10.4f}".format(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8],temp[8]))
	pfile.close()
	rsummary = summary
	rsummary.pop('model')

	mfile.write(str(rsummary))
	mfile.close()
	print ('\nWordcount:', summary['wordcount'],'\tAllwords:',summary['allwords'],'\nMaximum:',summary['mostfrequent'],'\ngrams:',summary['grams'])
	print ('Minimum:',summary['min'],'\tFreq:',summary['minfreq'],'\tTerm:',summary['minterm'],'\nallngrams:',summary['allngrams'])
	print ('Maximum:',summary['max'],'\tFreq:',summary['maxfreq'],'\tTerm:',summary['maxterm'])
	print ('Started:', started)
	ended = datetime.datetime.now()
	elapsed = ended - started
	print ('End    :', ended)
	print ('Elapsed:', elapsed)

def timer(spent):
	running = datetime.datetime.now()
	return running-spent

def summerize(model,transit,mostfrequent,wordcount,grams):
    	
	max,min,freq=0,100,0 ; minterm,maxterm='',''
	counter = 0 ; uniques = len(transit[1])
	lang =transit[0]
	for j,l in enumerate(transit[1]):
					 
		temp = [j+1, l[0],l[1],len(l[0]),transit[0]]
		counter+=l[1]
		j+=1
		if freq<l[1]: freq=l[1]		

		if max<len(l[0]): 
			max=len(l[0]) 
			maxterm = l[0]
			maxfreq = l[1]

		if (min>len(l[0])): 
			min = len(l[0]) 
			minterm = l[0]
			minfreq = l[1]
		model.append(temp)	
	
	grams[lang]= uniques
	mostfrequent[lang]=freq
	wordcount[lang] = counter
	allwords = sum(wordcount.values())
	allngrams = sum(grams.values())
	summary = dict(
					allngrams=allngrams,
					allwords=allwords,
					grams=grams,
					model=model,
					freq=freq,
					mostfrequent=mostfrequent,
					min=min,
					max=max,
					minterm=minterm,
					maxterm=maxterm,
					minfreq=minfreq,
					maxfreq=maxfreq,
					wordcount=wordcount,
					uniques=uniques
					)
	return summary

def wordgrams(listed):
    #ind to dicate considering frequency count	
	freTable=[]
	wordslists = set(listed[1])

	for item in wordslists:			
		if len(item)==0: continue
		i=0
		for items in listed[1]:	
			if len(items)==0: continue
			#if to_unicode(items)==to_unicode(item):	
			if items==item:	
				i+=1
		temps=[item,i]
		freTable.append(temps)

	freTable.sort(key = lambda nn:nn[1], reverse = True)
	return [listed[0],freTable]

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


def myclassifier(testing,frequencyTable,grams,wrongs,mytotal,myrecall,total):
	# q=0
	for i in testing: #[['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		# q+=1
		# if q==20: break
		for j in grams:
			id=classify(frequencyTable,j,i[1])
			if id[0]==1:continue
			check = 1 if i[0]==id[1] else 0			
			#r.write(str(j)+","+str(i[0])+","+str(id[1])+","+str(check)+","+str(id[2])+str('\r\n'))
			if check==0:
				wrongs[i[0]][id[1]][j]+=1
			
			mytotal[i[0]][j]+=1
			total[j]+=1
			myrecall[i[0]][j]+=check

def wrongclassifications(wrongs,wrongid,grams):
	for i in wrongs:
		for j in wrongs[i]:
			for g in grams:
				if wrongs[i][j][g]!=0:
					wrongid.append([i,j,g,wrongs[i][j][g]])
	return wrongid

def classify(frequencyTable,grams,sampled):
	lang = dict(am=0,ti=0,gu=0,ge=0,no=0)
	#added = dict(am=0,ti=0,gu=0,ge=0,no=0)
	ind=1 #to indicate the overflow of grams from max length of the ngram
	lang = lang.fromkeys(lang,0) #set all values of lang to 0
	norepeat = set() 
	for item in sampled: #['am', [['እው', 2], ['ውነ', 2], ['ነት', 2], ['እውነ', 3], ['ውነት', 3], ['እውነት', 4]]]
		#if l.to_unicode(item[0]) in norepeat: continue
		if item[0] in norepeat: continue
		if item[1]==grams:
			for items in frequencyTable:
				#if float(items[3])!=grams: continue
				#if l.to_unicode(items[1])==l.to_unicode(item[0]) and grams==item[1]:
				if items[1]==item[0] and grams==item[1]:
					lang[items[4]]+=float(items[8])
					ind=0
					norepeat.add(item[0])
	minimum = min(lang, key=lang.get)
	maximum = max(lang, key=lang.get)
	if minimum==maximum:
		return [ind,'no',lang]
	else:
		return [ind,maximum,lang]

def readsample(sample,phraselength=5):
	sampled=[]
	for i in sample:
		j = i.rstrip().split(',')
		temp = [j[0],j[1],j[2],j[3],j[4]] # [am,እውነት,1,4,82]
		if(int(j[2])==phraselength): 
			sampled.append(temp)
	return sampled