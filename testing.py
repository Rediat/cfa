import copy
import re

# lang = dict(am={},ge={},gu={},ti={})
# frequencyDict = copy.deepcopy(lang)
# inner = dict(freq=0,ovFreq=0)

# # for i in lang:
# # 	frequencyDict[i] = copy.deepcopy(inner)

# f=open('model.txt','r') #[am,ት ,2,2,78,1.0043572984749456,1.0009775171065494
# model = f.readlines()
# f.close()

# for temp in model: #[am,ት ,2,2,78,1.0043572984749456,1.0009775171065494,0.012987012987012988]
# 	temps = temp.rstrip('\n').split(',')
# 	frequencyDict[temps[0]][temps[1]]=dict(gram=temps[2],freq=temps[3],ovFreq=temps[6])

# # {'am': {'ት ': {'freq': '2', 'ovFreq': '1.0009551098376313'}

# print(frequencyDict)

s = "እውነት እላችኋለሁ ኀጢአት ስድብም ሁሉ ለሰው ልጆች ይሰረይላቸዋል"

for m in re.finditer(' ',s):
	print('space found',m.start())