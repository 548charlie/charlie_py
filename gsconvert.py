#!c:/python37/python
import os
import re
import sys
import subprocess
from pathlib import Path

def magicK(inFile, outFile):
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

def listfiles(indexFilename):
#    listOfFiles = list()
#    for (dirPath, dirNames, fileNames) in os.walk(path):
#        listOfFiles += [os.path.join(dirPath, file) for file in fileNames ] 
    count = 0
    fileTypes =[".jpg",".jpeg",".png",".bmp", ".JPG"] 
    file = open(indexFilename) 
    for line in file.readlines() :
        words = line.split("|")
        filePath = words[13].strip()  
        if filePath == "":
            continue

        suffix = Path(filePath).suffix
        if re.search(".pdf",suffix,re.I):
            count += 1
            outFile =getOutFile(filePath, suffix) 
            config = Path(outFile)
            if not config.exists(): 
                #command = ["c:\ImageMagick8bit\magick.exe","convert",filePath, outFile] 
                gsCommand = ["c:/gs926/bin/gswin32c.exe", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=tiffg4", "-dNOPAUSE", "-r400x400", f"-sOutputFile={outFile} ", filePath ] 
                cp = subprocess.run(gsCommand, stdout=subprocess.PIPE,stderr=subprocess.PIPE )
            
                if cp.returncode != 0:
                    print(f"Error: processing {filePath}{cp.stdout} {cp.stderr}   ") 
                else:
                    print(f"Success: {filePath} to {outFile} ") 
            else:
                print(f"File: {outFile} already exists ") 
        elif re.search(".jpg|.jpeg|.png|.bmp|.JPG", suffix, re.I): 
            count += 1
            outFile = getOutFile(filePath, suffix) 
            config = Path(outFile)
            if not config.exists(): 
                magicK(filePath, outFile) 
            else:
                print(f"File: {outFile} already exists ") 
        else:
            print(f"Error: file not defined Could not convert {filePath} with suffix of {suffix} "  )
    file.close() 
    print(count) 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide index file name with path") 
        exit
    else:
        indexFilename= sys.argv[1] 
        listfiles(indexFilename ) 
