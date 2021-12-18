#!c:/python37/python

import sys
import os
import re

def walk_dir(path, searchFor=" " ): 
    fileList =[] 
    pat = re.compile(searchFor, re.IGNORECASE) 
    for root, dir, files in os.walk(path):
        for file in files:
            if searchFor == "":
                fileList.append(os.path.join(root, file) )
            else:
                result = pat.search(file) 
                if result: 
                    fileList.append(os.path.join(root, file) )
    for f in fileList:
        print(f) 
    print(f"Number of files {len(fileList) } " ) 

if __name__ == '__main__':
    if len(sys.argv)  < 2:
        help = """Please enter path and regex of file name
            example: walk_dir.py c:\dinakar "junk"
            """
        print(help) 
        exit(0)  
    else:
        path = ""
        pattern = "" 
        if len(sys.argv) == 2:
            path = sys.argv[1]
            pattern = "" 
        else:
            path = sys.argv[1] 
            pattern = sys.argv[2] 
        print(pattern) 
        walk_dir(path, pattern) 
    
