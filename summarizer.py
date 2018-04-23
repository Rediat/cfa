import os
import sys
import re
import glob
import string
import datetime
import langid as l

#Todo
	#Complete the model for Naive Bayes and Frequency Rank classifiers
	#Generate other models considering the factors to consider for the test
	#include the timer() to measure the time complexity of processing

def wordlist():
	#****************** START Model generator ********************************
	print ("\n Loading corpus files to memory and generating models ... ")
	path = 'corpus/clearedcommons/300'
	mostfrequent = {} #the most frequent ngram in the corpus
	wordcount = {}
	grams = {}
	
	started = datetime.datetime.now()
	model =[]
	# print ("{}\t{}\t\t{}\t{}\t{}\t\t{}\t\t{}\t{}\t\t{}".format('seq','term','freq','gram','lang','prob','InFreq','OvFreq','percent'))

	for infile in glob.glob(os.path.join(path, '*.txt')): #opens files from director
		try:
			#Extract the file name			
			filename = infile.split('/')[-1]
			lang = filename[:2]

			#open and read file from corpus
			f=open(infile,'r', encoding = 'utf8' )
			rawtext = f.read()
			#rawtext = [lang,raw]
			f.close()

			#Word level parsing
			listed = regex(rawtext,lang).split()	

			summary = summerize(model,wordgrams(listed,lang),mostfrequent,wordcount,grams)

		except IOError:
			print ('Error: Can not open the file: ',lang)
			return	
	savetofile(summary, started)	

  #****************** END Model generator *******************************

def savetofile(summary, started):

	#model = [seq,term,freq,length,lang]
	#summary = dict(
	# #				allngrams=allngrams,
	# 				allwords=allwords,
	# 				grams=grams,
	# 				model=model,
	# 				freq=freq,
	# 				mostfrequent=mostfrequent,
	# 				min=min,
	# 				max=max,
	# 				minterm=minterm,
	# 				maxterm=maxterm,
	# 				minfreq=minfreq,
	# 				maxfreq=maxfreq,
	# 				wordcount=wordcount,
	# 				uniques=uniques
	
	if os.path.isfile('words.txt'): os.remove('words.txt')
	if os.path.isfile('summary.txt'): os.remove('summary.txt')
	
	wfile=open('words.txt','a+')
	mfile=open('summary.txt','a+')

	maximum = max(summary['mostfrequent'], key=summary['mostfrequent'].get)
	mysum = {'am':0,'gu':0,'ti':0,'ge':0}
	for i in summary['model']:
		mysum[i[4]] +=i[2]
		#temp = [i[0], i[1],i[2],i[3],i[4],i[2]/summary['wordcount'][i[4]],i[2]/summary['mostfrequent'][i[4]], i[2]/summary['mostfrequent'][maximum], mysum[i[4]]/summary['wordcount'][i[4]]]
		temp = [i[0], i[1],i[2],i[3],i[4],i[2]/summary['wordcount'][i[4]],i[2]/summary['grams'][i[4]]/summary['mostfrequent'][maximum], i[2]/summary['allngrams']/summary['mostfrequent'][maximum], mysum[i[4]]/summary['wordcount'][i[4]]]		
		wfile.write(str(temp[0])+","+str(temp[1])+","+str(temp[2])+","+str(temp[3])+","+str(temp[4])+","+str(temp[5])+","+str(temp[6])+","+str(temp[7])+str('\r\n'))
		# print ("{}\t{}\t\t{}\t{}\t{}\t\t{:10.4f}\t{:10.4f}\t{:10.4f}\t{:10.4f}".format(temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8]))
	wfile.close()
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

def wordgrams(listed,lang):
    #ind to dicate considering frequency count	
	freTable=[]
	wordslists = set(listed)

	for item in wordslists:			
		if len(item)==0: continue
		i=0
		for items in listed:	
			if len(items)==0: continue
			if to_unicode(items)==to_unicode(item):	
				i+=1
		temps=[item,i]
		freTable.append(temps)

	freTable.sort(key = lambda nn:nn[1], reverse = True)
	return [lang,freTable]

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

def regex(rawtext,lang):
	# lang=raw[0]
	# rawtext = raw[1]
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

def main():
	wordlist()
	#print (sys.stdout.encoding)
	
if __name__ == '__main__':
	main()