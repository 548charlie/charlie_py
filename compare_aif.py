#!c:/Python37/python

import csv
import sys
import os

#csv_file = open(file, mode"w") 
#csv_writer = csv.writer(cvs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#csv_write.writerow(array) 

def read_csv(filename) :
    rows = {}
    count = 0
    id = ""
    name = ""
    with open(filename) as csv_f:
        reader = csv.reader(csv_f)
        for row in reader:
            if row[0] == "TABLE ID":
                rows["column_names"] = row 
            if row[0] != "":
                id = row[0] 
                name = row[1] 
                count = 0
            if id in rows:
                new_id = id +"_" + str(count)
                count += 1
                row[1] = name 
                rows[new_id] = row
            else:
                row[1] = name 
                rows[id] = row
    return rows

def compare_rows(rows1, rows2,csv_filename):
    absent_in_second = {} 
    absent_in_first = {} 
    diffs = {} 
    for key, value1 in rows1.items():
        diff_vals = []
        for i in range(len(rows1["column_names"] )+1):
            diff_vals.append('') 
        if key in rows2:
            value2 = rows2[key]
            for idx, value in enumerate(value1):
                if value != value2[idx]: 
                    diff_vals[0] = key 
                    diff_vals[idx] = value + "<-->" +value2[idx] 
                    if diff_vals[1] == "":
                        diff_vals[1] = value1[1]  
                    diffs[key] = diff_vals 

        else:
            absent_in_second[key] =""
    for key , value in rows2.items():
        diff_vals = [] 
        for i in range(len(rows1["column_names"] )+1):
            diff_vals.append('') 
        if key in rows1:
            if not key in diffs:
                value1 = rows1[key]
                for idx, val in enumerate(value):
                    if val != value1[idx]:
                        diff_vals[0] = key 
                        diff_vals = value1[idx] +"<-->" + val
                        diffs[key] = diff_vals 
        else:
            absent_in_first[key] = "" 
    csv_file = open(csv_filename, mode="w",newline="\n")
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(rows1["column_names"]) 
    for key, value in diffs.items(): 
        csv_writer.writerow(value) 
    for key in absent_in_first :
        csv_writer.writerow(["Absent in first file",key] ) 
    for key in absent_in_second:
        csv_writer.writerow(["Absent in second file", key])

    csv_file.close() 
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Please provide two file names")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2] 
    rows1 = read_csv(file1)
    rows2 = read_csv(file2) 
    csv_filename = "compare_" +os.path.basename(file1)+"_" + os.path.basename(file2)  
    compare_rows(rows1, rows2,csv_filename) 
    comment = """ Please see {csv_filename} for comparison
        differences are shown as "value from first file <--> value from second file". Differences are listed within a column that are different. So you may have to scroll to the end in some cases"""
    print(f"{comment}" ) 
