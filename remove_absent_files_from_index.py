#!c:/python37/python

import os
import sys

def remove_absent_file(index_file):
    newfilename = "new_"+index_file
    newabfilename = "new_absent_records" 
    w = open(newfilename, "w+" ) 
    aw = open(newabfilename, "w+" ) 
    with open(index_file) as fif:
        for line in fif.readlines() :
            line = line.strip() 
            words = line.split("|" ) 
            filename = words[-1].strip()  
            if os.path.exists(filename) :
                w.write(line) 
                w.write("\n") 
            else:
                aw.write(line)  
                aw.write("\n" ) 
                
    aw.close() 
    w.close() 
        
    return 0




if __name__ == '__main__':
    print(f" length of arg {len(sys.argv) } " ) 
    if len(sys.argv) < 2:
        print("please give index file \n" ) 
    else:
        index_file = sys.argv[1] 
        remove_absent_file(index_file) 
