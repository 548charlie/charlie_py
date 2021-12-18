#!c:/Python37/python

import csv
import sys
import os
import re
#csv_file = open(file, mode"w") 
#csv_writer = csv.writer(cvs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#csv_write.writerow(array) 
#ignore_compare_vals = "PROFILE VARIABLES|PROFILE VARIABLE COMMENTS|INSTANT OF UPDATE|FILER DAEMON STATUS - DISPLAY|INSTANT OF ENTRY|INSTANT OF EDIT|STATUS MONITOR - LAST MESSAGE|STATUS MONITOR - MESSAGE COUNT|STATUS MONITOR - TIME SINCE LAST MSG|STATUS MONITOR - QUEUED EVENTS|STATUS MONITOR - QUEUED MSGS|STATUS MONITOR - WAITING MSGS|PORT|HL7_PID|COMMUNICATION START|INSTANT|FILER_EVENT START INSTANT|COMMUNICATION DAEMON STATUS - DISPLAY|FILER DAEMON STATUS - DISPLAY|CONTACT DATE|PORT"
ignore_compare_vals = "AUTOSTART|AUTOSTART TIME OUT|AUTOSTART TIME OUT EMAIL|AUTOSTART TIME OUT NO WARNING|COMM PROCESS|COMMUNICATION DAEMON STATUS - DISPLAY|COMMUNICATION START|CONTACT DATE|CUSTOM|CUSTOM COMMUNICATIONS|CUSTOM FILER|DATA|DATA MODEL|DATA MODEL POPULATION CODE|DATA MODEL POPULATION CODE RECORD NAME|DATA MODEL RECORD NAME|DISPLAY|EVENT PROCESSES|FILER|FILER DAEMON STATUS - DISPLAY|FILER_EVENT START INSTANT|HL7_PID|HOSTNAME|INSTANT|INSTANT OF EDIT|INSTANT OF ENTRY|INSTANT OF UPDATE|NO VALIDATION - EMP ID SETTING REASON|NO VALIDATION - EMP ID SETTING REASON RECORD NAME|PORT|PROFILE VARIABLE COMMENTS|PROFILE VARIABLES|QUERY|RUN ON SHADOW|SEGMENT OVERRIDE|SEGMENT OVERRIDE (DISPLAY ONLY)|SEGMENT OVERRIDE (DISPLAY ONLY) RECORD NAME|START INTERFACE|STATUS|STATUS MONITOR|STATUS MONITOR - LAST MESSAGE|STATUS MONITOR - MESSAGE COUNT|STATUS MONITOR - QUEUED EVENTS|STATUS MONITOR - QUEUED MSGS|STATUS MONITOR - TIME SINCE LAST MSG|STATUS MONITOR - WAITING MSGS|SURESCRIPT|VALIDATION|VALIDATION - COMPARE NAME|VALIDATION - VALIDATE RESUBMIT|XML|XML PASSWORD|XML USERNAME|^192|^220000001|^220000003|^22000001|^940276|^940319|^9403391|^940600|^940606|^940607|^940608|^940616|^940624|^940628|^940632|^940642|^940643|^940650|^940651|^940703|^940710|^940750|^940761|^940803|^940807|^940900|^940901|^940903|^940990|^99940101|^99940343|^99940901|^XML" 
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

def compare_rows(rows1, rows2,csv_filename):
    csv_file = open(csv_filename, mode="w",newline="\n")
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["Record ID","Record Name", "Col Name", "First File", "second File"] )  
    col_names = rows1["column_names"] 
    absent_in_first = {}
    absent_in_second= {} 
    common_keys = {} 
    for key, value in rows1.items():
        if key == "column_names" :
            continue
        name = value.pop(0) 
        if re.search(ignore_compare_vals, key, re.IGNORECASE):
            continue
        if key in rows2:
            common_keys[key] = "" 
            svalue = rows2[key]
            name = svalue.pop(0) 
            value = "\n".join(value) 
            svalue =  "\n".join(svalue) 
            if value != svalue:
                keys = key.split("=")
                line = [keys[0], name, keys[1]  ] 
                line.extend([value, svalue] ) 
                csv_writer.writerow(line) 
                #print(f"{keys} ")  
        else:
            value.insert(0, name) 
            absent_in_second[key] = value
    for key, value in rows2.items():
        if key == "column_names":
            continue
        name = value.pop(0) 
        if key in common_keys:
            continue
        if re.search(ignore_compare_vals, key, re.IGNORECASE):
            continue
        if key in rows1:
            svalue = rows1[key]
            name = svalue.pop(0) 
            value = "\n".join(value)
            svalue =  "\n".join(svalue)  
            if value != svalue:
                keys = key.split("=") 
                line = [keys[0], name, keys[1]  ] 
                line.extend([ svalue,value]) 
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
        help = """
Usage:  python compare_aip.py file1.csv file2.csv INI_type [AIP] 
Example: python compare_aip.py relb_aip.csv rel_aip.csv AIP 
Both files are csv files in the above example and output will be csv file
===========================
Following is an example on how to use JXPORT in Epic and
what options to choose for this program to work
RELB>d main^JXPORT
INI: AIP-Interface Profile
Import spec:
Item(s): all
Put multiple response data into a single row (per record)? no
Export null data as <NULL>? No
Hide unused items? No
Include category validation? No
Export category names? Yes
Include INI validation? No
Export raw data (unpadded .1) for networked items? yes
Export networked record names in adjacent columns? yes
Export networked record private external IDs? No
Protect sheet structure? No
Profile Recs: all
Use last DAT? Yes
===================================
fetch xml file from the server
Open xml file with MS Excel program and save it as csv files.
At present output it sent to the file written to current directory.
Make sure you have write permissions in the current directory.
Open the output with MS Excel. Only differences are shown.
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
