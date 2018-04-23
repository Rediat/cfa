import langid as l
import os
import copy

def main():
	# language = dict(am='Amharic',ge='Geez',gu='Guragigna',ti='Tigrigna')
	s=open('model.txt','r')
	model = s.readlines()

	os.system('clear') # on linux 

	counts = {} ; grams = (2,3,4,5)
	lang = dict(am=0,ge=0,gu=0,ti=0)
	
	for i in grams:
		counts[i] = copy.deepcopy(lang)

	# print (counts)
	counter=0
	for temp in model: #[am,ት ,2,2,78,1.0043572984749456,1.0009775171065494,0.012987012987012988]
		temps = temp.rstrip('\n').split(',')
		# print (temps[2],temps[0])
		# if int(temps[2])==5:
		# if temps[0]=='am' and int(temps[2])==4:
		# 	counter+=int(temps[3])
		counts[int(temps[2])][temps[0]]+=int(temps[3])
	
	# print(counter)
	for i in grams:
		# for j in lang:
		print('Grams {:<3}\t {}'.format(i,counts[i]))

if __name__ == '__main__':
	main()