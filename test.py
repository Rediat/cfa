import sys
import copy

def main():
# 	temp = 'እውነት'
# 	print(sys.getsizeof(sys.getsizeof))
# 	print(sys.getsizeof(str('እውነት')))
# 	print(sys.getsizeof(temp))

	# 
	maxngram = 5

	grams=[]
	for i in range(2,maxngram+1):
		grams.append(i)
	print (grams)
if __name__ == '__main__':
	main()