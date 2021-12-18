#!/Python37/python
import glob
from shutil import copy2
from shutil import move
import os.path
print("Hello world" ) 

def copy_move(): 
    source="y:/conversions/upa/final_prd_extract_2019/wip/index_files"
    cp_dest = "Y/conversions/upa/tst/onbase_pdf " 
    mv_dest = cp_dest + "/done" 
    src_files = glob.glob(source +"/index.*.txt" ) 

    count =1
    for file in src_files:
        (path, name) = os.path.split(file)  
        copy2(file, cp_dest) 
        move(file, mv_dest + "/"+name ) 
        if count == 100:
            break
        count += 1

if __name__ == "__main__":
    copy_move() 
