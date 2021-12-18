#!c:/Python37/python

import csv
import sys
import os
import re
note_compare = """
NOTE ABOUT ignore_compare_vals:  Please try to enter full column name from the JXPORT file if it is partial name, it may  filter some other column that matches partial name. Names are separated by |
"""
ignore_compare_vals = "PROFILE VARIABLES|PROFILE VARIABLE COMMENTS|INSTANT OF UPDATE|FILER DAEMON STATUS - DISPLAY|INSTANT OF ENTRY|INSTANT OF EDIT|STATUS MONITOR - LAST MESSAGE|STATUS MONITOR - MESSAGE COUNT|STATUS MONITOR - TIME SINCE LAST MSG|STATUS MONITOR - QUEUED EVENTS|STATUS MONITOR - QUEUED MSGS|STATUS MONITOR - WAITING MSGS|PORT|HL7_PID|COMMUNICATION START|INSTANT|FILER_EVENT START INSTANT|COMMUNICATION DAEMON STATUS - DISPLAY|FILER DAEMON STATUS - DISPLAY|CONTACT DATE|PORT"

def read_csv(filename, column_name) :

    rows = {}
    count = 0
    id = ""
    name = ""
    collect = 0
    col_names = [] 
    key = ""
    value = ""
    with open(filename) as csv_f:
        reader = csv.reader(csv_f)
        for row in reader:
            if row[0].strip()  == column_name:
                rows["column_names"] = [element.strip() for element in  row] 
                col_names = [elem.strip() for elem in  row]
                collect = 1
            if collect == 1 :
                if row[0] != "":
                    id = row[0].strip()   
                    name = row[1].strip()  
                    for idx, val in enumerate( row):
                        key = id + "="+ col_names[idx] 
                        value = val.strip() 
                        if value == "":
                            continue
                        if re.search("of profile variable", col_names[idx], re.IGNORECASE ):
                            continue
                        if re.search("profile variables record name", col_names[idx], re.IGNORECASE ):
                            key = id +"="+ "profile_"+ value
                            value = row[idx +1].strip() 
                        if key in rows:
                            row[0] = id
                            row[1] = name
                            rows[key].append(value)  
                        else:
                            row[0] = id 
                            row[1] = name 
                            rows[key] = [name, value] 
                else:
                     for idx, val   in enumerate( row):
                        value = val.strip() 
                        if value == "":
                            continue
                        key = id + "="+col_names[idx]
                        if re.search("of profile variable", col_names[idx], re.IGNORECASE ):
                            continue

                        if re.search("profile variables record name", col_names[idx], re.IGNORECASE ):
                            key = id +"="+ "profile_"+value
                            value = row[idx +1].strip() 
                            
                        if key in rows:
                            row[0] = id
                            row[1] = name
                            rows[key].append(value)  
                        else:
                            row[0] = id 
                            row[1] = name 
                            rows[key] = [name, value]  
                key = ""
                value = ""
    return rows
def compare_column(col_1, col_2):
    tmp1 = [x for x in col_1 if x not in col_2]
    tmp2 = [ x for x in col_2 if x not in col_1]
    return (tmp1, tmp2) 

def compare_rows(rows1, rows2,csv_filename):
    csv_file = open(csv_filename, mode="w",newline="\n")
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["Record ID","Record Name", "Col Name", "First File", "second File"] )  
    col_names = rows1["column_names"] 
    absent_in_first = {}
    absent_in_second= {} 
    common_keys = {} 
    for key, value in rows1.items():
        name = value.pop(0) 
        if re.search(ignore_compare_vals, key, re.IGNORECASE):
            continue
        if key in rows2:
            common_keys[key] = "" 
            svalue = rows2[key]
            name = svalue.pop(0) 
            col_1, col_2 = compare_column(value, svalue) 
            col_1 = "\n".join(col_1)
            col_2 = "\n".join(col_2) 
            if col_1 != col_2:
                keys = key.split("=")
                line = [keys[0], name, keys[1]  ] 
                line.extend([col_1, col_2] ) 
                csv_writer.writerow(line) 
        else:
            value.insert(0, name) 
            absent_in_second[key] = value
    for key, value in rows2.items():
        name = value.pop(0) 
        if key in common_keys:
            continue
        if re.search(ignore_compare_vals, key, re.IGNORECASE):
            continue
        if key in rows1:
            svalue = rows1[key]
            name = svalue.pop(0) 
            col_2, col_1 = compare_column(value, svalue) 
            col_1 = "\n".join(col_1)
            col_2 = "\n".join(col_2) 
            #if value != svalue:
            if col_1 != col_2:
                keys = key.split("=") 
                line = [keys[0], name, keys[1]  ] 
                line.extend([ col_1,col_2]) 
                csv_writer.writerow(line) 
                #print(f"{keys} ") 
        else:
            value.insert(0, name) 
            absent_in_first[key]= value
  
    for key, value in absent_in_first.items():
        name = value.pop(0) 
        pval = key.split("=")  
        line = [pval[0], name,pval[1]   ] 
        val = "\n".join(value) 
        line.extend(["Absent",val] )
        csv_writer.writerow(line ) 
    for key, value in absent_in_second.items():
        name = value.pop(0) 
        pval =key.split("=")
        line =[pval[0], name, pval[1]  ] 
        val = "\n".join(value) 
        line.extend([val, "Absent"] )
        csv_writer.writerow(line ) 

    csv_file.close() 
if __name__ == "__main__":
    if len(sys.argv) != 4:
        help = f"""
Usage:  python compare_aip.py file1.csv file2.csv INI_type [AIP AIF WQF CER LLB IIT ORD RFL] 
Example: python compare_aip.py relb_aip.csv rel_aip.csv AIP 
Both files are csv files in the above example and output will be csv file
===========================
Following is an example on how to use JXPORT in Epic and
what options to choose for this program to work
RELB>d main^JXPORT
INI: AIP 
Import spec: <return>
Item(s): all 
Put multiple response data into a single row (per record)? no
Export null data as <NULL>? No
Hide unused items? No
Export category names? Yes
Export raw data (unpadded .1) for networked items? yes
Export networked record names in adjacent columns? yes
Export networked record private external IDs? No
Protect sheet structure? No
Specifications: all
File name: /epic/90day/aip_poc_dsd_20190620 (this is an example name) 
===================================
fetch xml file from the server
Open xml file with MS Excel program and save it as csv files.
At present output it sent to the file written to current directory.
Make sure you have write permissions in the current directory.
Open the output with MS Excel. Only differences are shown. You can save the csv file as Excel work sheet which will maintain all formatting and filters etc.
\n
{note_compare} 
====================================
Author: Dinakar Desai, Ph.D.
Date: May 30, 2013
Updated on : June 8, 2019
If you experience any problems with the program, please contact above author.
        """
        print(help) 
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2] 
        ini = sys.argv[3] 
        if ini == "AIF":
            column_name = "TABLE ID"
        elif ini == "AIP":
            column_name = "PROFILE RECORD"
        elif ini == "WQF":
            column_name = "WORKQUEUE ID"
        elif ini == "CER":
            column_name = "RULE ID"
        elif ini == "LLB":
            column_name = "LAB ID"
        elif ini == "IIT":
            column_name = "TYPE ID"
        elif ini == "RFL":
            column_name = "REFERRAL ID"
        elif ini == "ORD":
            column_name = "ORDER ID"
        rows1 = read_csv(file1, column_name) 
        rows2 = read_csv(file2, column_name) 
        csv_file1, ext = os.path.splitext(os.path.basename(file1))
        csv_file2, ext = os.path.splitext(os.path.basename(file2)) 
        csv_filename = "compare_" +csv_file1+"_" + csv_file2  + ext  
        compare_rows(rows1, rows2,csv_filename) 
        ignore_list = ignore_compare_vals.split("|")
        ignore_items = "\n".join(ignore_list)
        comment = f""" Please see {csv_filename} for comparison
differences are shown as between first file and second file in their own columns. Only differences are shown \n
    we have filterred following values and will not show up in output\n {ignore_items} """
        print(f"{comment}" ) 
