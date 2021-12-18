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
    cp = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode != 0:
        errcode =cp.stderr.decode("utf-8") 
        print(f"Error: processing {inFile} to {outFile} {cp.stdout} {cp.stderr} {errcode} "  )
    else:
        print(f"Success:{inFile} to {outFile}  ") 

def getOutFile(fileName, suffix):
    filename = Path(fileName) 
    outFile = filename.with_suffix('.tiff').name
    return outFile
    
def hello(input, output):
    print(input,"-->", output)

def get_files(path, searchFor ):    
    fileList = list()
    files = list() 
    for(dirPath,dirNames,fileNames) in os.walk(path):
        fileList += [os.path.join(dirPath, file) for file in fileNames ]
    pattern = re.compile(searchFor, re.IGNORECASE) 
    for fileName in fileList:
        if pattern.search(fileName):
            files.append(fileName) 
    return files

def convert(listOfFiles) :
    listOfProcs = []
    procs = 15 
    tasks = [listOfFiles[i:i+procs] for i in range(0, len(listOfFiles),procs )  ]
    for task in tasks:
        for inFile in task:
            stopFile = "stopme"
            fileInfo = Path(stopFile )
            if fileInfo.exists():
                os.remove(stopFile) 
                return

            suffix = Path(inFile).suffix
            outFile = getOutFile(inFile, suffix)
            outinfo = Path(outFile) 
            if outinfo.exists():
                continue
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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide path to files and type of file to convert") 
        print("""
                This program can convert png, jpeg, jpg, pdf, bmp to tiff
                It will convert all files mentioned above in the path
                and  including subfolders. It will not overwrite or 
                delete any files.
                It will not convert if the tiff file already exists.
                The converted file will be in the same directory as the
                original file.

                if you want to stop the program gracefully in the middle
                of big job or using thousands of files to convert. 
                Create a file called stopme in the current directory
                (directory where you started this program from. It w) 
                convert_to_tiff.py path extension_to_convert
                example: convert_to_tiff.py c:/junk "png$|pdf$|jpg$" 
                
                Author: Dinakar Desai, Ph.D.
                Date: Nov 4, 2019
                Please contact me if you want to report bugs and/or enhancements
                """ ) 
        exit
    else:
        path = sys.argv[1] 
        searchFor = sys.argv[2] 
        files=get_files(path, searchFor )  
        convert(files) 
