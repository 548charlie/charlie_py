#!c:/Python37/python

import csv
import sys
import os
import re
from pathlib import Path
def read_csv(filename, aif_file) :
    rows = {}
    count = 0
    id = ""
    name = ""
    profile_col=0
    value_col = 0
    file_info = Path(filename) 
    aif_info = Path(aif_file)
    aif_id_name = {} 
    if aif_info.exists():
        with open(aif_file) as aif_fh:
            aif_reader = csv.reader(aif_fh)
            for aif_row in aif_reader:
                if aif_row[0] != "":
                    aif_id_name[aif_row[0] ] = aif_row[1]

    if file_info.exists(): 
        csv_file = open("table_by_aip.csv", mode="w",newline="\n")
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Interface ID", "Interface Name", "Profile Variable", "Table ID", "Table Name"] ) 

        with open(filename) as csv_f:
            reader = csv.reader(csv_f)
            for row in reader:
                if row[0] == "PROFILE RECORD":
                    rows["column_names"] = row 
                if row[0] != "":
                    interface_id = row[0] 
                    interface_name = row[1] 
                    col_name="PROFILE VARIABLES RECORD NAME"
                    for i, cname in enumerate(row):
                        if cname == col_name:
                            profile_col = i
                            value_col = i+1
                    count =0

                    profile_name = row[profile_col]
                    profile_value = row[value_col] 
                    table_name = ""
                    if re.search("TBL|TABLE|TAB", profile_name, re.IGNORECASE):
                        if profile_value in aif_id_name:
                           table_name = aif_id_name[profile_value]  
                        print(f" {interface_id} {interface_name} {profile_name} {profile_value} {table_name} "    ) 
                        csv_writer.writerow([interface_id, interface_name,profile_name, profile_value, table_name]) 
                else:
                    profile_name = row[profile_col]
                    profile_value = row[value_col] 
                    table_name = ""
                    if re.search("TBL|TABLE|TAB", profile_name, re.IGNORECASE):
                        if profile_value in aif_id_name:
                            table_name = aif_id_name[profile_value]  

                        csv_writer.writerow([interface_id, interface_name,profile_name, profile_value, table_name])
                        print(f" {interface_id} {interface_name} {profile_name} {profile_value} {table_name} "    ) 
        csv_file.close() 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"""Please provide AIP Jxport csv file and AIF JXport file name.
            AIP JXport csv file is used to get profile variables
            AIF JXport csv file is used to get able names from .1""")
    else:
        aip_file = sys.argv[1]
        aif_file = sys.argv[2] 
        rows1 = read_csv(aip_file, aif_file)
        csv_filename = "table_by_aip.csv"  
        comment = f""" Please see {csv_filename} for comparison
        differences are shown as "value from first file <--> value from second file". Differences are listed within a column that are different. So you may have to scroll to the end of row in some cases"""
        print(f"{comment}" )
