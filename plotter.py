import matplotlib.pyplot as plt ; import copy; from matplotlib import style ; import csv ; import os ; import glob ; import numpy as np

# style.use('fivethirtyeight')
# To do:
#	Share the y axis for comparing individual meausres for each classifier
	
def main():
	os.system('clear')
	selection=1 ; phraselength = [1,2,3,4,5,10,15,20,25]

	models = {'bl':{}, 'by':{}, 'fl':{}, 'in':{}, 'il':{}}
	classifiertype = {1:'bl', 2:'by', 3:'fl', 4:'in', 5:'il'}
	phrasemapping = {1:0, 2:1, 3:2, 4:3, 5:4, 10:5, 15:6, 20:7, 25:8}
	labels = {'bl':'Baseline', 'by':'N-grams from text - Byteorder', 'fl':'Fixel Length with Location', 'in':'Infinity n-grams', 'il':'Infinity n-grams with Location'}
	measures = dict(accuracy=[0,0,0,0,0,0,0,0,0],precision=[0,0,0,0,0,0,0,0,0],recall=[0,0,0,0,0,0,0,0,0],fscore=[0,0,0,0,0,0,0,0,0])
	classifiers = dict(CFA={},NBC={})
	classifiersb = dict(CFA={},NBC={})
	modelsb = {2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}, 8:{}, 9:{}, 10:{}, 11:{}, 12:{}}
	
	# classifiertypes = {1:{},2:{},3:{},4:{},5:{},6:{},7:{},8:{},9:{},10:{}}

	for i in models:
		models[i] = copy.deepcopy(measures)

	for i in range(2,13):
		modelsb[i] = copy.deepcopy(models)

	for i in classifiersb:
		classifiersb[i] = copy.deepcopy(modelsb)

	# print (classifiersb);return

	#classifiers {'CFA': {'bl': {'accuracy': [], 'precision': [], 'recall': [], 'fscore': []}, 'by': {'accuracy': [], 'precision': [], 'recall': [], 'fscore': []}, 
	for i in classifiers:
		classifiers[i] = copy.deepcopy(models)
	
	path1='result/ov/' ; filename1='summary.txt'
	if os.path.isfile(os.path.join(path1,filename1)): os.remove(os.path.join(path1,filename1))
	r=open(os.path.join(path1,filename1),'a+')
	for ct in range(1,11):
		path = 'result/ov/'+str(ct)+'/' ; files = '*.txt'
		for infile in glob.glob(os.path.join(path, files)): 
			try:
				filename = infile.split('/')[-1]		
				with open(os.path.join(path, filename),'r') as csvfile:
					plots = csv.reader(csvfile,delimiter=',')
					for i in plots: #CFA,1,bl,1,2030,0.8177339901477833,0.8200209546225121,0.820284772167601,0.8201528421795917
						# print (ct,i[0],i[2],i[5],i[6],i[7],i[8],i[3],phrasemapping[int(i[3])])#classifiers[i[0]][i[2]]['accuracy'][phrasemapping[int(i[3])]])
						r.write(str(ct)+","+str(i[0])+","+str(i[2])+","+str(i[4])+","+str(i[5])+","+str(i[6])+","+str(i[7])+","+str(i[8])+","+str(i[3])+str('\r\n'))
						classifiers[i[0]][i[2]]['accuracy'][phrasemapping[int(i[3])]]+=(float(i[5])/10)
						classifiers[i[0]][i[2]]['precision'][phrasemapping[int(i[3])]]+=(float(i[6])/10)
						classifiers[i[0]][i[2]]['recall'][phrasemapping[int(i[3])]]+=(float(i[7])/10)
						classifiers[i[0]][i[2]]['fscore'][phrasemapping[int(i[3])]]+=(float(i[8])/10)
			except IOError:
				print ('Error: Can not open the file: ',filename) 
				return
	else:
		r.close()
	
	path1='result/av/' ; filename1='summary.txt'
	if os.path.isfile(os.path.join(path1,filename1)): os.remove(os.path.join(path1,filename1))
	r=open(os.path.join(path1,filename1),'a+')
	for ct in range(1,11):
		path = 'result/av/'+str(ct)+'/' ; files = '*.txt'
		for infile in glob.glob(os.path.join(path, files)): 
			try:
				filename = infile.split('/')[-1]		
				with open(os.path.join(path, filename),'r') as csvfile:
					plots = csv.reader(csvfile,delimiter=',')
					for i in plots: #CFA,1,bl,1,2030,0.8177339901477833,0.8200209546225121,0.820284772167601,0.8201528421795917
						# print (ct,i[0],i[2],i[5],i[6],i[7],i[8],i[3],phrasemapping[int(i[3])],i[9])#classifiers[i[0]][i[2]]['accuracy'][phrasemapping[int(i[3])]])
						# if int(i[9])>5:continue
						r.write(str(ct)+","+str(i[0])+","+str(i[2])+","+str(i[4])+","+str(i[5])+","+str(i[6])+","+str(i[7])+","+str(i[8])+","+str(i[3])+","+str(i[9])+str('\r\n'))
						classifiersb[i[0]][int(i[9])][i[2]]['accuracy'][phrasemapping[int(i[3])]]+=(float(i[5])/10)
						classifiersb[i[0]][int(i[9])][i[2]]['precision'][phrasemapping[int(i[3])]]+=(float(i[6])/10)
						classifiersb[i[0]][int(i[9])][i[2]]['recall'][phrasemapping[int(i[3])]]+=(float(i[7])/10)
						classifiersb[i[0]][int(i[9])][i[2]]['fscore'][phrasemapping[int(i[3])]]+=(float(i[8])/10)
			except IOError:
				print ('Error: Can not open the file: ',filename) 
				return
	else:
		r.close()

	# print('classifiersb {}'.format(classifiersb)) ; return

	cselector = {1:'CFA',2:'NBC'} ; selector = 1
	while selection!=0:	
		os.system('clear') # on linux 
		ngtype=1
		print ('\n\n{}'.format('='*100))
		print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - PLOTTER'.center(100,' '))
		print ('-'*100)	

		ngtype = int(input('\nSelect N-gram usage type number below: \n\n   1. All Fixed Length N-grams \n   2. Individual Fixed Length N-grams \n   3. Exit\t:   '))
		if ngtype==3: selection=0 ;return
		else:
			classifier = int(input('\nSelect Classifier type number below: \n\n   1. Cumulative Frequency Addition (CFA) \n   2. Naive Bayes Classifier (NBC) \n   3. Exit\t:   '))
		
		if classifier==3: selection=0 ;return
		elif classifier<0 or classifier>3:
			print ('\nPlease check your entry above and try again.')
			pause=input(''); print('{}'.format(pause)) ; continue
		else:		
			classifierselector=cselector[classifier]
			# 1. bl. The Model is based on Fixed Length N-grams without location features - Baseline.
			# 2. by. The Model is based on source text - Byteorder Ngrams.
			# 3. fl. The Model is based on Fixed Length N-grams with location features.
			# 4. in. The Model is based on Infiniti-grams without location features.
			# 5. il. The Model is based on Infiniti-grams with location features.
			choice=1
			while choice!=0:
				os.system('clear') # on linux
				ind=1; ng=2
				print ('\n\n{}'.format('='*100))
				print ('AUTHOMATIC LANGUAGE IDENTIFIER USING CUMMULATIVE FREQUENCY ADDITION - PLOTTER'.center(100,' '))
				print ('-'*100)	
				if ngtype==2:
					ng = int(input('\nSelect The N-gram number below {}: \n\n   2. N=2 \n   3. N=3 \n   4. N=4 \n   5. N=5 \n   6. N=(2-5) \n   7. Go Back\t: '))				
				if ng==7: break
				measure = int(input('\nSelect Measure type number below: \n\n   1. Accuracy \n   2. Precision \n   3. Recall \n   4. F-score    \n   5. Change Classifier   \n   6. All in One Model   \n   7. Go Back\t:   '))
				if measure==5: break
				elif measure==7: break
				else:
					# if 	measure!=6:
					selector = int(input('\nSelect Model type number below for {}: \n\n   1. The Model is based on Fixed Length N-grams without location features - Baseline [bl] \n   2. The Model is based on source text - Byteorder N-grams [by] \n   3. The Model is based on Fixed Length N-grams with location features [fl] \n   4. The Model is based on Infiniti-grams without location features [in] \n   5. The Model is based on Infiniti-grams with location features [il] \n   6. Change Model  \n   7. Exit\t: '.format(classifierselector)))				
					if selector == 6: break
					elif selector == 7: return
					elif measure<6:
						if ngtype==1:
							ind = int(input('\nSelect Comparisions type number below: \n\n   1. Witin a Classifier across Language Models \n   2. Same Language Model Across Classifiers\t:   '))
						else:
							ind = int(input('\nSelect Comparisions type number below: \n\n   1. Witin a Classifier across Language Models \n   2. Same Language Model Across Classifiers \n   3. Same Language Model Across N-grams\t\t:   '))							
				
				if measure<0 or measure>6 or selector<1 or selector>7 or ind<1 or (ngtype==2 and ind>3) or (ngtype==1 and ind>2):
					print ('\nPlease check your selection above and try again.')
					pause=input(''); print('{}'.format(pause))
				else:
					mod=classifiertype[selector]
					plt.xlabel('Phrase Length')

					if measure == 1:
						plt.ylabel('Accuracy')
						if ind==1:
							if ngtype==1:
								plt.title('{} Accuracy over test phrase length'.format(classifierselector))
								plt.plot(phraselength,classifiers[classifierselector]['bl']['accuracy'],label=labels['bl'])
								plt.plot(phraselength,classifiers[classifierselector]['by']['accuracy'],label=labels['by'])
								plt.plot(phraselength,classifiers[classifierselector]['fl']['accuracy'],label=labels['fl'])
								plt.plot(phraselength,classifiers[classifierselector]['in']['accuracy'],label=labels['in'])
								plt.plot(phraselength,classifiers[classifierselector]['il']['accuracy'],label=labels['il'])
							else:
								plt.title('{} Accuracy over test phrase length on {}-grams'.format(classifierselector,ng))
								plt.plot(phraselength,classifiersb[classifierselector][ng]['bl']['accuracy'],label=labels['bl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['by']['accuracy'],label=labels['by'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['fl']['accuracy'],label=labels['fl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['in']['accuracy'],label=labels['in'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['il']['accuracy'],label=labels['il'])
						
						elif ind==2:
    							
							if ngtype==1:
								plt.title('Accuracy over test phrase length')
								plt.plot(phraselength,classifiers['CFA'][mod]['accuracy'],label='CFA - '+labels[mod])  
								plt.plot(phraselength,classifiers['NBC'][mod]['accuracy'],label='NBC - '+labels[mod])
							else:  
								plt.title('Accuracy over test phrase length {}-grams'.format(ng))
								plt.plot(phraselength,classifiersb['CFA'][ng][mod]['accuracy'],label='CFA - '+labels[mod])  
								plt.plot(phraselength,classifiersb['NBC'][ng][mod]['accuracy'],label='NBC - '+labels[mod])
						else:
								plt.title('{} Accuracy over test phrase length on across n-grams'.format(classifierselector))
								plt.plot(phraselength,classifiersb[classifierselector][2][mod]['accuracy'],label='{} {}-grams'.format(labels[mod],2))
								plt.plot(phraselength,classifiersb[classifierselector][3][mod]['accuracy'],label='{} {}-grams'.format(labels[mod],3))
								plt.plot(phraselength,classifiersb[classifierselector][4][mod]['accuracy'],label='{} {}-grams'.format(labels[mod],4))
								plt.plot(phraselength,classifiersb[classifierselector][5][mod]['accuracy'],label='{} {}-grams'.format(labels[mod],5))
		
					elif measure == 2:						
						plt.ylabel('Precision')
						if ind==1:
							if ngtype==1:
								plt.title('{} Precision over test phrase length'.format(classifierselector))
								plt.plot(phraselength,classifiers[classifierselector]['bl']['precision'],label=labels['bl'])
								plt.plot(phraselength,classifiers[classifierselector]['by']['precision'],label=labels['by'])
								plt.plot(phraselength,classifiers[classifierselector]['fl']['precision'],label=labels['fl'])
								plt.plot(phraselength,classifiers[classifierselector]['in']['precision'],label=labels['in'])
								plt.plot(phraselength,classifiers[classifierselector]['il']['precision'],label=labels['il'])
							else:
								plt.title('{} Precision over test phrase length on {}-grams'.format(classifierselector,ng))
								plt.plot(phraselength,classifiersb[classifierselector][ng]['bl']['precision'],label=labels['bl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['by']['precision'],label=labels['by'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['fl']['precision'],label=labels['fl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['in']['precision'],label=labels['in'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['il']['precision'],label=labels['il'])	
						
						elif ngtype==2:
							
							if ngtype==1:
								plt.title('Precision over test phrase length')
								plt.plot(phraselength,classifiers['CFA'][mod]['precision'],label='CFA - '+labels[mod]) 
								plt.plot(phraselength,classifiers['NBC'][mod]['precision'],label='NBC - '+labels[mod])
							else:  
								plt.title('Precision over test phrase length {}-grams'.format(ng))
								plt.plot(phraselength,classifiersb['CFA'][ng][mod]['precision'],label='CFA - '+labels[mod])  
								plt.plot(phraselength,classifiersb['NBC'][ng][mod]['precision'],label='NBC - '+labels[mod])
						else:
								plt.title('{} Precision over test phrase length on across n-grams'.format(classifierselector))
								plt.plot(phraselength,classifiersb[classifierselector][2][mod]['precision'],label='{} {}-grams'.format(labels[mod],2))
								plt.plot(phraselength,classifiersb[classifierselector][3][mod]['precision'],label='{} {}-grams'.format(labels[mod],3))
								plt.plot(phraselength,classifiersb[classifierselector][4][mod]['precision'],label='{} {}-grams'.format(labels[mod],4))
								plt.plot(phraselength,classifiersb[classifierselector][5][mod]['precision'],label='{} {}-grams'.format(labels[mod],5))

					if measure==3:
						plt.ylabel('Recall')
						if ind==1:
							if ngtype==1:
								plt.title('{} Recall over test phrase length'.format(classifierselector))    								
								plt.plot(phraselength,classifiers[classifierselector]['bl']['recall'],label=labels['bl'])
								plt.plot(phraselength,classifiers[classifierselector]['by']['recall'],label=labels['by'])
								plt.plot(phraselength,classifiers[classifierselector]['fl']['recall'],label=labels['fl'])
								plt.plot(phraselength,classifiers[classifierselector]['in']['recall'],label=labels['in'])
								plt.plot(phraselength,classifiers[classifierselector]['il']['recall'],label=labels['il'])
							else:
								plt.title('{} Recall over test phrase length on {}-grams'.format(classifierselector,ng))
								plt.plot(phraselength,classifiersb[classifierselector][ng]['bl']['recall'],label=labels['bl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['by']['recall'],label=labels['by'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['fl']['recall'],label=labels['fl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['in']['recall'],label=labels['in'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['il']['recall'],label=labels['il'])
						
						elif ind==2:
							
							if ngtype==1:
								plt.title('Recall over test phrase length')
								plt.plot(phraselength,classifiers['CFA'][mod]['recall'],label='CFA - '+labels[mod]) 
								plt.plot(phraselength,classifiers['NBC'][mod]['recall'],label='NBC - '+labels[mod])
							else:
								plt.title('Recall over test phrase length {}-grams'.format(ng))
								plt.plot(phraselength,classifiersb['CFA'][ng][mod]['recall'],label='CFA - '+labels[mod])  
								plt.plot(phraselength,classifiersb['NBC'][ng][mod]['recall'],label='NBC - '+labels[mod])
						else:
								plt.title('{} Recall over test phrase length on across n-grams'.format(classifierselector))
								plt.plot(phraselength,classifiersb[classifierselector][2][mod]['recall'],label='{} {}-grams'.format(labels[mod],2))
								plt.plot(phraselength,classifiersb[classifierselector][3][mod]['recall'],label='{} {}-grams'.format(labels[mod],3))
								plt.plot(phraselength,classifiersb[classifierselector][4][mod]['recall'],label='{} {}-grams'.format(labels[mod],4))
								plt.plot(phraselength,classifiersb[classifierselector][5][mod]['recall'],label='{} {}-grams'.format(labels[mod],5))

					elif measure==4:
						plt.ylabel('F-score')
						if ind==1:
							if ngtype==1:
								plt.title('{} F-score over test phrase length'.format(classifierselector))    								
								plt.plot(phraselength,classifiers[classifierselector]['bl']['fscore'],label=labels['bl'])
								plt.plot(phraselength,classifiers[classifierselector]['by']['fscore'],label=labels['by'])
								plt.plot(phraselength,classifiers[classifierselector]['fl']['fscore'],label=labels['fl'])
								plt.plot(phraselength,classifiers[classifierselector]['in']['fscore'],label=labels['in'])
								plt.plot(phraselength,classifiers[classifierselector]['il']['fscore'],label=labels['il'])
							else:
								plt.title('{} F-score over test phrase length on {}-grams'.format(classifierselector,ng))
								plt.plot(phraselength,classifiersb[classifierselector][ng]['bl']['fscore'],label=labels['bl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['by']['fscore'],label=labels['by'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['fl']['fscore'],label=labels['fl'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['in']['fscore'],label=labels['in'])
								plt.plot(phraselength,classifiersb[classifierselector][ng]['il']['fscore'],label=labels['il'])
						
						elif ind==2:
							
							if ngtype==1:
								plt.title('F-score over test phrase length')
								plt.plot(phraselength,classifiers['CFA'][mod]['fscore'],label='CFA - '+labels[mod]) 
								plt.plot(phraselength,classifiers['NBC'][mod]['fscore'],label='NBC - '+labels[mod])
							else:
								plt.title('F-score over test phrase length {}-grams'.format(ng))
								plt.plot(phraselength,classifiersb['CFA'][ng][mod]['fscore'],label='CFA - '+labels[mod])  
								plt.plot(phraselength,classifiersb['NBC'][ng][mod]['fscore'],label='NBC - '+labels[mod])
						else:
								plt.title('{} F-score over test phrase length on across n-grams'.format(classifierselector))
								plt.plot(phraselength,classifiersb[classifierselector][2][mod]['fscore'],label='{} {}-grams'.format(labels[mod],2))
								plt.plot(phraselength,classifiersb[classifierselector][3][mod]['fscore'],label='{} {}-grams'.format(labels[mod],3))
								plt.plot(phraselength,classifiersb[classifierselector][4][mod]['fscore'],label='{} {}-grams'.format(labels[mod],4))
								plt.plot(phraselength,classifiersb[classifierselector][5][mod]['fscore'],label='{} {}-grams'.format(labels[mod],5))
					
					elif measure==6:
						plt.ylabel('{} Measures'.format(labels[mod]))
						if ngtype==1:
							plt.title('{} Measures over test phrase length'.format(classifierselector))
							# plt.plot(phraselength,classifiers[classifierselector][mod]['accuracy'],label='Accuracy')
							plt.plot(phraselength,classifiers[classifierselector][mod]['precision'],label='Precision')
							plt.plot(phraselength,classifiers[classifierselector][mod]['recall'],label='Recall')
							plt.plot(phraselength,classifiers[classifierselector][mod]['fscore'],label='F-score')
						else:
							plt.title('{} Measures over test phrase length on {}-grams'.format(classifierselector,ng))
							# plt.plot(phraselength,classifiersb[classifierselector][ng][mod]['accuracy'],label='Accuracy')
							plt.plot(phraselength,classifiersb[classifierselector][ng][mod]['precision'],label='Precision')
							plt.plot(phraselength,classifiersb[classifierselector][ng][mod]['recall'],label='Recall')
							plt.plot(phraselength,classifiersb[classifierselector][ng][mod]['fscore'],label='F-score')

					elif measure==7: selection=0 ; break
					
					plt.grid(color='gray',linestyle='dotted',linewidth=0.2)
					plt.legend(loc='best',shadow=True, fontsize='small')
					plt.show()

if __name__ == '__main__':
	main()