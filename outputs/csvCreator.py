import os
import sys

if __name__ == "__main__":
	f = []
	for (dirpath, dirnames, filenames) in os.walk("/home/chettyharish/workspace/temp/silent-stores/outputs"):
	    f.extend(filenames)
	
	f = [x for x in f if os.path.splitext(x)[1] == ".txt"]
	
	for file in f:
		ofn = str(os.path.splitext(file)[0]) + ".csv"
		print(ofn)
		ofn = open(ofn , "w")
		for line in file:
			line = ",".join(line.split()) + "\n"
			ofn.write(line)
		ofn.close()
		