#!c:/python37/python
import sys
import os
import shutil
def get_file_size(index_file, src_dir, dst_dir):
    linecount = 0
    totalfilesize = 0
    index = 1
    lines = [] 
    gb = 1024*1024*1024
    with open(index_file) as ifh:
        for line in ifh.readlines():
            linecount += 1
            line = line.strip() 
            words = line.split("|") 
            filename = words[-1] 
            file_stat = os.stat(filename) 
            file_size = file_stat.st_size
            totalfilesize += file_size
            gb_size = totalfilesize/gb
            print(f"file_size {file_size} totalfilesize {totalfilesize} gb_size {gb_size} linecount {linecount} index {index} " ) 
            lines.append(line) 
            if gb_size > 1 or linecount == 10:
                print(f"gb_size {gb_size} " ) 
                index_filename = "index_"+ str(index) 
                index += 1
                write_index_file(index_filename,lines, src_dir, dst_dir) 
                lines = []  
                linecount = 0
                totalfilesize = 0
            if index > 4:
                return

def write_index_file(index_file, lines, src_dir,dst_dir):
    src_base =  r"\\efsbus1\RhapBatchData\tch\conversions\upa\final_prd_extract_2019"
    src_dir = os.path.join(src_dir, index_file) 
    print(f" src_dir {src_dir} " ) 
    if not os.path.exists(src_dir):
        os.makedirs(src_dir, exist_ok=True) 
    idx_filename = os.path.join(src_dir, index_file+".txt") 
    print(f"idx_filename {idx_filename} " ) 

    with open(idx_filename, "a") as ofh:
        for line in lines:
            words = line.split("|") 
            filename =words[-1] 
            dir_name = os.path.dirname(filename) 
            basename = os.path.basename(filename) 
            final_filename = filename.replace(src_base, dst_dir) 
            src_name = dir_name.replace(src_base, src_dir  ) 
            print(f"dir_name {dir_name} src_name {src_name}\nbasename {basename}  " ) 
            dst_filename = os.path.join(src_name, basename)  
            print(f"dst_filename {dst_filename} " ) 
            if os.path.exists(filename):
                if not os.path.exists(src_name):
                    os.makedirs(src_name, exist_ok=True) 
                print(f"copy filename {filename} src_name {src_name}  " )               
                if not os.path.exists(dst_filename):  
                    shutil.copy(filename, dst_filename) 
            words[-1]= final_filename
            line = "|".join(words)
            ofh.write(line)  
            ofh.write("\n" ) 



if __name__ == "__main__":
   
    help="""
    This program takes large index file and splits the file into
    multiple files based on the size of the files that index file 
    references. Either number of lines equal to 1000 or total file
    size is greater than 19 GB (1024*1024*1024) 
    At the end of program you will have index file with name like index_1.txt
    and a directory like index_1/images at src_dir level and that directory
    contains all files that are referenced in the index_1.txt. same 
    will be true for index_2.txt etc

    example:
    index_file_by_file_size.py <index_file> <src_dir> <dst_dir>
    index_file_by_file_size index.txt \\\\tst\\junk \\\\tchserver\\somedir
    Then to process the files by onbase, move the index file from
    src_dir to onbase index file and move all images present in 
    index_*\images directory to dst_dir/images

    Author: Dinakar Desai, Ph.D.
    Date: November 22, 2019

    Please let me know if you experience any problem with the program
    or if you find a bug or need any improvement to the program. This
    program is written for some specific application.
    
    """  
    if len(sys.argv)  < 4:
        print(help) 
        exit(0) 
    else:
        index_file = sys.argv[1] 
        src_dir = sys.argv[2] 
        dst_dir = sys.argv[3] 
        get_file_size(index_file, src_dir, dst_dir) 
