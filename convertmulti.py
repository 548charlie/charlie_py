#!c:/python37/python
import os
import re
import sys
import subprocess
from pathlib import Path
import multiprocessing

def gsConvert(inFile, outFile):
   gsCommand = ["c:/gs926/bin/gswin32c.exe", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=tiffg4", "-dNOPAUSE", "-r400x400", f"-sOutputFile={outFile} ", inFile ] 
   cp = subprocess.run(gsCommand, stdout=subprocess.PIPE,stderr=subprocess.PIPE )
            
   if cp.returncode != 0:
    print(f"Error: processing {inFile}{cp.stdout} {cp.stderr}   ") 
   else:
    print(f"Success: {inFile} to {outFile} ") 

def magicConvert(inFile, outFile):
    command = ["c:/ImageMagick7/magick.exe", "convert","-colors", "254", inFile, outFile]
    cp = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        errcode =cp.stderr.decode("utf-8") 
        print(f"Error: failed to convert {inFile} to {outFile} with errcode {errcode} "  )
    else:
        print(f"Success: converting {inFile} to {outFile}  ") 

def getOutFile(file, suffix):
    outFile = file.replace(suffix, ".tiff") 
    return outFile
def hello(input, output):
    print(input,"-->", output)

def listfiles(indexFilename):
#    listOfFiles = list()
#    for (dirPath, dirNames, fileNames) in os.walk(path):
#        listOfFiles += [os.path.join(dirPath, file) for file in fileNames ] 
    count = 0
    listOfFiles = [] 
    with open(indexFilename) as idFile:
        for line in idFile.readlines():
            words = line.split("|")
            if len(words) < 13:
                print("Error: fewever elements:", words)
                continue
            filePath = words[13].strip()
            if filePath == "":
                continue
            listOfFiles.append(filePath) 
    listOfProcs = []
    procs = 20
    tasks = [listOfFiles[i:i+procs] for i in range(0, len(listOfFiles),procs )  ]
    for task in tasks:
        for inFile in task:
            print("Count:", count)
            count += 1
            suffix = Path(inFile).suffix
            outFile = getOutFile(inFile, suffix)
            fileInfo = Path(outFile)
            if not fileInfo.exists():
                if re.search(".pdf", suffix, re.I):
                    p = multiprocessing.Process(target=gsConvert, args=(inFile, outFile) )
                    p.start()
                    listOfProcs.append(p)
                elif re.search(".jpg|.jpeg|.png|.bmp|.JPG", suffix, re.I): 
                    p = multiprocessing.Process(target=magicConvert, args=(inFile, outFile) )
                    p.start()
                    listOfProcs.append(p)
        for p in listOfProcs:
            p.join()
    print(count) 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide index file name with path") 
        exit
    else:
        indexFilename= sys.argv[1] 
        listfiles(indexFilename ) 
