#!c:/python37/python
import sys
import os

print("Hello World" ) 




def split_index_file(index_file, dst_dir):
    print(f" file {index_file} dst_dir {dst_dir}  " ) 
    count = 0
    with open(index_file) as fh:
        for line in fh.readlines():
            line = line.strip()
            words = line.split("|" )
            filename = words[-1]
            (dir, basefilename) =os.path.split(filename)  
            (basename, ext) = os.path.splitext(basefilename)  
            file_stat = os.stat(filename) 
            file_size = file_stat.st_size/(1024*1024) 

            print(f"basename {basename} ext {ext} size {file_size}  " ) 
            count += 1
            if count == 10:
                break
    return














if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Please provide the index file and destination directory" )
    else:
        print(f"got all arguments {len(sys.argv) } " ) 
        index_file = sys.argv[1]
        dst_dir = sys.argv[2]
        split_index_file(index_file, dst_dir) 

