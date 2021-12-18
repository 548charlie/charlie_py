#!c:/python37/python

import os,sys
from pathlib import Path
import os
import re
import datetime
import shutil
from pathlib import Path
import subprocess

def getValidLines(keyFile, index_file):
    (name, ext) = os.path.splitext(index_file)
    newIdxFile = name + "_valid_files" + ext
    fw = open(newIdxFile, "w")
    fileNames = dict() 
    with open(keyFile) as kf:
        for line in kf.readlines():
            words= line.split(":")
            if len(words) >= 2:
                keyFilename =words[1]
                keyFilename = keyFilename.strip()
                if not keyFilename in fileNames:
                    fileNames[keyFilename] = 1
                else:
                    fileNames[keyFilename] +1

    with open(index_file) as indf:
        for line in indf.readlines():
            words = line.split("|")
            if len(words) >= 13:
                filename = words[13]
                filename = filename.strip()
                if not filename in fileNames:
                    fw.write(line) 

    fw.close() 
def gettime():
    now =datetime.datetime.today().strftime("%Y%m%d%H%M%S")
    return now
def changeExt(filename, toExt):
    (name, ext) = os.path.splitext(filename)
    output = name +"_new" + ext
    fw = open(output, "w+")
    with open(filename) as fr:
        for line in fr.readlines():
            words =line.split("|")
            if len(words)>= 13:
                pdffile = words[13] 
                (name, ext) =  os.path.splitext(pdffile)
                newname = name + toExt
                words[13] = newname
                fw.write("|".join(words) )
                fw.write("\n") 

    fw.close() 
def listFiles(filename,preAbs):
    count = 0
    with open (filename) as f:
        for line in f.readlines():
            words = line.split("|")
            if len(words) < 13:
                print(line)
            else:
                fName = words[13].strip() 
                fileInfo = Path(fName) 
                if preAbs == "present":
                    if fileInfo.exists():
                        print(f"Present:{gettime() }  {fName } ") 
                else:
                    if not fileInfo.exists():
                        print(f"Absent: {gettime() } {fName}" ) 

def findLine (filename, searchStr):
    count =0 
    fileInfo = Path(filename)
    if not fileInfo.exists():
        print(f"{gettime() }:{filename} file does not exists  ") 
        return
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip() 
            if re.search(searchStr, line, re.I):
                print(count, ":", line)
            count += 1

def file_ops(filename, op="copy" ) :
    with open(filename) as fh:
        for line in fh.readlines():
            line = line.strip() 
            if line.startswith("#" ):
               continue
            (src_file, dst_file) = line.split(":::")  
            src_file = src_file.strip() 
            dst_file = dst_file.strip() 
            src_info = Path(src_file)  
            src_base = os.path.basename(src_file) 
            dst_base = os.path.basename(dst_file) 
            if src_info.exists():
                if op == "copy": 
                    abs_path = os.path.dirname(dst_file) 
                    dst_path_info = Path(dst_file) 
                    if os.path.isdir(abs_path):
                        print(f"copy {src_file} to {dst_file}  " ) 
                        shutil.copyfile(src_file, dst_file) 
                    else:
                        print(f"Directory {abs_path} does not exist " ) 
                elif op == "move" :
                    abs_path = os.path.dirname(dst_file) 
                    dst_path_info = Path(dst_file) 
                    if os.path.isdir(abs_path):
                        print(f"move {src_file} to {dst_file}   " ) 
                        shutil.move(src_file, dst_file) 
                    else:
                        print(f"Directory {abs_path} does not exist " ) 
            else:
                print(f" File {src_file} does not exist " ) 


def count_page_number(index_file):
    count = 0
    with open(index_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            filename = line.split("|" )[-1]
            if os.path.isfile(filename): 
                command = ["c:/ImageMagick7/magick.exe", "identify",filename]
                cp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                wc_process = subprocess.Popen(['c:/gow/bin/wc.exe', '-l'],stdin=cp.stdout, stdout=subprocess.PIPE) 
                cp.stdout.close() 
                out, error = wc_process.communicate() 
                path_list = os.path.normpath(filename).split(os.path.sep)
                words = ",".join(path_list)
                words = words + "," + str(out.strip(),"utf-8" )  
                page_count = str(out.strip(),"utf-8")  
                now = gettime() 
                print(f"{count}, {now},{filename},{page_count}" ) 
                count += 1
            else:
                print(f"file does not exist {filename} ") 


def split_file(count,filename):
    lineCnt = 0
    (fname_prefix, ext) =os.path.splitext(filename )  
    fcnt = 1
    print(f"{gettime() }: {fname_prefix}_{str(fcnt) }{ext}  ")
    with open(filename) as f:
        for line in f.readlines()  :
            if lineCnt == 0:
                w = open(fname_prefix + "_" +str(fcnt) +ext, "w")  
            if lineCnt < count:
                w.write(line) 
                lineCnt += 1
            else:
                lineCnt = 0
                fcnt +=1
                w.close() 
if __name__ == "__main__":
    help ="""Usage: misc.py  [find|split|list|ext|fileexist|file_op] [stringToSearch|1000|[present|absent]|move|copy".tiff"|keyfilename ]  <file_to_split>|list_of_files
Example: misc split 1000 index.txt 
    Above example will split index.txt into multiple files with 1000 lines
    in each file and name of the files will be indix_[n].txt where n is the 
    number starting with 1
Example: misc.py find something index.txt
    Above example will find the something text in index.txt file and if found
    will display the line number and text

Example: misc.py list absent <filename>
    Above example works only on special format file
example: misc.py ext ".tiff" index.txt
    above example will work with very specific file but will change the extension to ".tiff" 
Example: misc.py fileexist keyFilename index.txt
    Above example will work with very specific file and will not check file exists or not because files not existing are given in keyFile
Example: misc.py file_op move filename
    Above example will take a "filename"  which contains list of files to be moved from one place to next. filename will have entry like as follows:
    "c:\dinakar\junk\test.txt"  to "c:\dinakar\tst.txt" 
    quotes are not required if there is no space in the path
    file_op can move or copy. More functionality will be added later on


    Author: Dinakar Desai, Ph.D.
    Date: March 20, 2019""" 
        
    if len(sys.argv) <4 :
        print(f"{gettime() }:{ help}") 
        exit
    else:
        what = sys.argv[1] 
        if what == "split":
            count = int(sys.argv[2])
            print(count) 
            filename = sys.argv[3] 
            fileInfo = Path(filename) 
            if fileInfo.exists() :
                split_file(count, filename ) 
            else:
                print(f"{filename} file does not exists" ) 
        elif what == "find":
            searchFor = sys.argv[2]
            filename = sys.argv[3] 
            findLine(filename, searchFor) 
        elif what == "list":
            preAbs = sys.argv[2] 
            filename = sys.argv[3] 
            listFiles(filename, preAbs) 
        elif what == "ext":
            newExt = sys.argv[2]
            filename = sys.argv[3]
            changeExt(filename, newExt) 
        elif what == "fileexist" :
            keyFile = sys.argv[2]
            idFile = sys.argv[3]
            getValidLines(keyFile, idFile) 
        elif what == "file_op":
            op = sys.argv[2] 
            filename = sys.argv[3] 
            file_ops(filename,op) 
        elif what == "count":
            filename = sys.argv[2]
            count_page_number(filename) 
