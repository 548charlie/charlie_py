#!c:/Python32/python
import csv
import os
import sys
import shutil
import glob
if (len(sys.argv) != 2 ): 
    print("Usage: ", sys.argv[0], " <Part name_of the file>" )
    print "If full name is given then only one file is processed "
    print "other wise it will process all files that matches the pattern"
    print "script is run from csv directory and it is assumed that  "
    print "wip and csvdone directory exist and files will be moved there "
    print "for further processing"
    exit(0)  

filename=sys.argv[1] 
files=glob.glob("*" + filename + "*")
for filename in files:

    if not os.path.exists(filename):
        print(filename, " file does not exist, please check for file name")
        continue 
    file = open(filename) 
    reader = csv.reader(file, delimiter='|')
    csv_file, ext = os.path.splitext(filename)
    csv_file = "../wip/" + csv_file +"." + "csv"
    csv_fh = open(csv_file, 'a') 
    line_num=0
    for line in reader:
        count =15 
        keep=0
        for c in range(15, len(line) ): 
            count += 1
            if keep == 0 and line[c] != "" :
                keep= 1
                break

        if keep == 1:
            kline="|".join(line)
            csv_fh.write(kline)
            csv_fh.write("\n") 
    file.close()
    csv_fh.close()
    dst="../csvdone/" + filename
    if os.path.exists(dst) :
        print dst + " exists"
    else:
        shutil.move(filename, dst ) 
