#!c:/python37/python

import os
import re
import sys

def listfiles(path,searchFor):
    listOfFiles = list()
    for (dirPath, dirNames, fileNames) in os.walk(path):
        listOfFiles += [os.path.join(dirPath, file) for file in fileNames ] 
    count = 0
    for file in listOfFiles:
        if re.search(searchFor, file):
            print(f"{file} " ) 
            count += 1

    print(count) 

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide directory to list files and searchFor") 
        print("Example: c:/dinakar <look_for_tst in file name" ) 
        exit
    else:
        
        listfiles(sys.argv[1],sys.argv[2] ) 
