import os
import sys
import re
import glob
import string
import datetime
import langid as l

#Todo
	#Consider multilingual testing samples
	#include the timer() to measure the time complexity of processing

def sampling():
		#****************** START Model generator ********************************
	os.system('clear') # on linux
	print ("\nLoading testing files to memory and generating testing samples ... ")
	path = 'corpus/clearedcommons/10'
	totals = 0 #dict(am=0,ti=0,gu=0,ge=0,no=0)
	started = datetime.datetime.now()
	
	if os.path.isfile('sample.txt'): os.remove('sample.txt')
	for infile in glob.glob(os.path.join(path, '*.txt')): #opens files from director
		try:
			#Extract the file name			
			filename = infile.split('/')[-1]
			lang = filename[:2]
			
			f=open(infile,'r', encoding = 'utf8' )
			raw = f.read()
			f.close()

			#Word level parsing
			listed = regexs(raw,lang).strip()
			
			k=0; t=[0]; i=0; length = len(listed)

			while i in range(length):
				j=listed.find(' ',listed.find(' ')+k)
				if j==-1:
					t.append(length)
					break
				t.append(j)
				k=j;i+=1

			test = []
			maxlength = 10
			for x,i in enumerate(t):
				for j in t:
					if(j>=t[x]):continue
					temp = listed[j:t[x]].strip()
					length = len(temp.split())
					if length>maxlength: continue
					temps = [lang,temp,sys.getsizeof(temp)]
					test.append(temps)
					
			f=open('sample.txt','a+')	
			for temp in test:
				#[lang,string,number of words,number of characters,bytes]
				f.write(str(temp[0])+","+str(temp[1])+","+str(len(temp[1].split()))+","+str(len(temp[1].strip()))+","+str(temp[2])+str('\r\n'))
				totals+=1
			f.close()
		except IOError:
			print ('Error: Can not open the file: ',lang)
			return
	
	print ('{} Test strings are successfuly created in Sample.txt.'.format(totals))
	print ('\nStarted:', started)
	ended = datetime.datetime.now()
	elapsed = ended - started
	print ('End    :', ended)
	print ('Elapsed:', elapsed)
	print ('\n')

cpdef regexs(rawtext, lang='am'):
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

cpdef main():
	sampling()

if __name__ == '__main__':
	main()