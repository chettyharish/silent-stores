import os
import sys

if __name__ == "__main__":
	f = []
	path = "/home/chettyharish/workspace/temp/silent-stores/outputs/benchmark_RLE"
	for (dirpath, dirnames, filenames) in os.walk(path):
	    f.extend(filenames)
 	
	f = [x for x in f if os.path.splitext(x)[1] == ".txt"]
 	
	for file in f:
		ofn = str(os.path.splitext(file)[0]) + ".csv"
		print(ofn)
		ofn = open(ofn , "w")
		for line in open(path + "/" + file , "r"):
			line = ",".join(line.split()) + "\n"
			ofn.write(line)
		ofn.close()
		