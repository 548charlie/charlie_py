#!/usr/bin/env python3


#########################################################
# Program Name: compare_msg
# Purpose: compare_msg program compares messages from two files that have
#           same sequence of messages stored as new line terminated messages.
#           if the sequence is out of order, all messages comparison may be 
#           wrong. This progam compares example hl7 by every field and displays
#           fields that are differen.
#   
#           if the output file is given results will be written to file as csv.
#
#
#
#Parameters:
#   input_file1 : first file name
#   input_file2 :second file name
#   output_file : optional, if given it will write to file otherwise to stdout
#
#
#$Author:$ Dinakar Desai (Please do not remove author name or modify it)
#$Date:$ Sat Dec 22 09:39:19 CST 2007
#
#
#
#############################################################
import sys
import os
def usage(prog_name ):
    text="""Usage: {}  input_file1 input_file2 [output_file <optional>]
    Example {} test1 prod1 test_prod
    Above example compares test1 file contents to prod1 contents and puts results
    in test_prod file
    """.format(prog_name,prog_name )
    print(text )
    exit
def compare_fields(fields1, fields2 ):
    isdiff = 0  
    seg=fields1[0]
    fld_diffs = []
    if len(fields1) <= len(fields2 ):
        for j, fld2 in enumerate(fields2 ):
            if j < len(fields1 ):
                fld1=fields1[j]
                if fld1 != fld2:
                    fld_diffs.append(f"{seg}|{j}|{fld1}|{fld2}")
    else:
        for j, fld1 in enumerate(fields1 ):
            if j < len(fields2 ):
                fld2 = fields2[j]
                if fld1 != fld2:
                    fld_diffs.append(f"{seg}|{j}|{fld1}|{fld2}" )
    return fld_diffs

def compare_messages(msg1, msg2 ):
    segments1=msg1.split('\r')
    segments2=msg2.split('\r')
    seg_dict1={}
    seg_dict2={}
    fldsep=segments1[0][3]
    cmpsep=segments1[0][4]
    seg_idx=0
    isdiff=0
    if len(segments1 ) <= len(segments2 ):
        for i, segment2 in enumerate(segments2 ):
            fields2=segment2.split(fldsep)
            if i < len(segments1):
                segment1=segments1[i]
                fields1=segment1.split(fldsep) 
                fld_diffs=compare_fields(fields1, fields2 )
                if len(fld_diffs ) >0:
                    print(f"{segment1}\n{segment2}" )
                    for value in fld_diffs:
                        print(f"{value }" )
            else:
                print(f"Extra Segment in second File: {segment2 }" )
                    
    else:
        for i, segment1 in enumerate(segments1 ):
            fields1=segment1.split(fldsep)
            if i < len(segments2 ):
                segment2=segments2[i]
                fields2=segment2.split(fldsep)
                fld_diffs=compare_fields(fields1, fields2 )
                if len(fld_diffs ) >0:
                    print(f"{segment1}\n{segment2}" )
                    for value in fld_diffs:
                        print(f"{value }" )
            else:
                print(f"Extra Segments in first File: {segment1}" )
    text="""
            seg2=fields2[0] 
            seg_idx=fields2[1]
            fld_diffs=[]
            if i < len(segments1 ):
                segment1=segments1[i]
                fields1=segment1.split(fldsep)
                seg1 = fields1[0]
                if seg1 != seg2:
                    print(f"{seg1 } and {seg2} are different")
                    continue
                else:
                    if len(fields1) <= len(fields2 ):
                        for j, fld2 in enumerate(fields2 ):
                            if j < len(fields1 ):
                                fld1=fields1[j]
                                if fld1 != fld2:
                                    fld_diffs.append(f"{seg1}|{j}|{fld1}|{fld2}")
                                    isdiff = 1
                    else:
                        for j, fld1 in enumerate(fields1 ):
                            if j < len(fields2 ):
                                fld2 = fields2[j]
                                if fld1 != fld2:
                                    fld_diffs.append(f"{seg1}|{j}|{fld1}|{fld2}" )
                                    isdiff = 1
                    if isdiff :
                        print(f"{segment1}\n{segment2}" )
                        for value in fld_diffs:
                            print(f"{value}" )
                        print("" )
                    isdiff=0
    else:
        for i, segment1 in enumerate(segments1 ):
            fields1=segment1.split(fldsep)
            seg1=fields1[0] 
            fld_diffs = []
            if i < len(segments2 ):
                segment2=segments2[i]
                fields2=segment2.split(fldsep)
                seg2 = fields2[0]
                if seg1 != seg2:
                    print(f"{seg1 } and {seg2} are different")
                    continue
                else:
                    if len(fields1) <= len(fields2 ):
                        for j, fld2 in enumerate(fields2 ):
                            if j < len(fields1 ):
                                fld1=fields1[j]
                                if fld1 != fld2:
                                    fld_diffs.append(f"{seg1}|{j}|{fld1}|{fld2}")
                    else:
                        for j, fld1 in enumerate(fields1 ):
                            if j < len(fields2 ):
                                fld2 = fields2[j]
                                if fld1 != fld2:
                                    fld_diffs.append(f"{seg1}|{j}|{fld1}|{fld2}")
                    if isdiff:
                        print(f"{segment1}\n{segment2}" )
                        for value in fld_diffs:
                            print(f"{value}" )
                        print("")
                    isdiff = 0

        """


def process_messages(file1, file2 ):
    messages1 =[]
    messages2=[]
    with open(file1,newline='\r\n') as fh1:
        for line in fh1:
            line = line.strip()
            messages1.append(line)
    with open(file2, newline='\r\n') as fh2:
        for line in fh2:
            line = line.strip()
            messages2.append(line)
    if len(messages1 ) != len(messages2 ):
        print(f"Number of messages different in two files {len(messages1 ) } and {len(messages2 ) }")
    if len(messages1 ) <= len(messages2 ):
        for index, msg2 in enumerate(messages2):
            if index < len(messages1 ):
                msg1=messages1[index ]     
                compare_messages(msg1, msg2 )
    else:
        for index, msg1 in enumerate(messages1):
            if index < len(messages2 ):
                msg2=messages2[index ]     
                compare_messages(msg1, msg2 )

if __name__ == '__main__':
    if len(sys.argv) < 3:
        prog_name= sys.argv[0]
        usage(prog_name )
    else:
        file1=sys.argv[1]
        file2=sys.argv[2]
        if os.path.isfile(file1 )and os.path.isfile(file2 ):
           process_messages(file1, file2 )
        else:
            print(f"{file1 } or {file2 }  does not exists" )
            usage(prog_name )

