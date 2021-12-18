#!c:/python37/python
import os
import re
import sys
import subprocess
from pathlib import Path
import threading

def gsConvert(inFile, outFile):
    outFileInfo = Path(outFile)
    inFileInfo = Path(inFile)
    if outFileInfo.exists():
        print(f"Success: File exists: {outFile} ") 
        return
    if not inFileInfo.exists():
        print(f"Error: File does not Exists: {inFile}  ")
        return 


    gsCommand = ["c:/gs926/bin/gswin32c.exe", "-q", "-dBATCH", "-dNOPAUSE", "-sDEVICE=tiffg4", "-dNOPAUSE", "-r400x400", f"-sOutputFile={outFile} ", inFile ] 
    cp = subprocess.run(gsCommand, stdout=subprocess.PIPE,stderr=subprocess.PIPE )
            
    if cp.returncode != 0:
        print(f"Error: processing {inFile} to {outFile} {cp.stdout} {cp.stderr}   ") 
    else:
        print(f"Success:{inFile} to {outFile} ") 

def magicConvert(inFile, outFile):
    outFileInfo = Path(outFile)
    inFileInfo = Path(inFile)
    if outFileInfo.exists():
        print(f"Success: File exists: {outFile} ") 
        return
    if not inFileInfo.exists():
        print(f"Error: File does not Exists: {inFile}  ")
        return 


    command = ["c:/ImageMagick7/magick.exe", "convert","-colors", "254", inFile, outFile]
    command = ["c:/ImageMagick7/magick.exe", inFile, outFile] 
    cp = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        errcode =cp.stderr.decode("utf-8") 
        print(f"Error: processing {inFile} to {outFile} {cp.stdout} {cp.stderr} {errcode} "  )
    else:
        print(f"Success:{inFile} to {outFile}  ") 

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
            if len(words) < 14:
                print("Error: fewever elements:", words)
                continue
            filePath = words[14].strip()
            (dir, ext) = os.path.splitext(filePath)
            if (ext == ".png" ):
                if filePath == "":
                    continue
                listOfFiles.append(filePath) 
    listOfProcs = []
    procs = 150 
    tasks = [listOfFiles[i:i+procs] for i in range(0, len(listOfFiles),procs )  ]
    for task in tasks:
        for inFile in task:
            count += 1
            stopFile = "stopme"
            fileInfo = Path(stopFile )
            if fileInfo.exists():
                os.remove(stopFile) 
                return

            suffix = Path(inFile).suffix
            (dir, ext) =os.path.splitext(inFile) 
            outFile = dir + ".pdf"  

            if re.search(".pdf", suffix, re.I):
                p = threading.Thread(target=gsConvert, args=(inFile, outFile) )
                p.start()
                listOfProcs.append(p)
            elif re.search(".jpg|.jpeg|.png|.bmp|.JPG", suffix, re.I): 
                p = threading.Thread(target=magicConvert, args=(inFile, outFile) )
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
