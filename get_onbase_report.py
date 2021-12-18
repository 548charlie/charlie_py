#!/opt/bin/python3.7
import glob
import re
import os


def get_report(filelist):
    reg = re.compile("^TOTALS" ) 
    for file in filelist:
        time = ""
        records= 0
        pages = 0
        batch = 0 
        basename="" 
        with open(file) as fh:
            count = 1 
            for line in fh.readlines():
                line = line.strip() 
                if count == 3: 
                    time=line 
                if reg.search(line) :
                    (totals,records, pages)=line.split() 
                if re.search("^File.\s+:" , line ):
                    filename = line.split(":")[1].split()[0] 
                    basename = filename.split("\\")[-1] 
                if re.search("Internal Batch Number", line ):
                    batch = line.split(":" )[1] 
                count += 1
        print(f"{time},{basename},{records},{pages},{batch} " ) 


if __name__ == '__main__':
    filelist = glob.glob("*.txt") 
    get_report(filelist) 
