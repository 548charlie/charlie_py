#!c:/python39/python.exe

import sys
import os

def compare_messages(file1, file2 ):
    messages1=[]
    messages2=[]

    with open(file1 ) as fh1:
        for line in fh1:
            line=line.strip()
            if line.startswith('MSH' ):
                continue
            messages1.append(line)
    with open(file2 ) as fh2:
        for line in fh2:
            line=line.strip()
            if line.startswith('MSH' ):
                continue

            messages2.append(line )
    unmatched=[]
    common=[]
    for i, elem in enumerate(messages1):
        if elem in messages2:
            common.append(f"{elem }--{elem}")
        else:
            common.append(f"{elem}--" )
    
    for i, elem in enumerate(messages2):
        if elem in messages1:
            if f"{elem}--{elem}" not in common:
                common.append(f"{elem }--{elem}")
        else:
            unmatched.append(f"    --{elem}" )
    #matched segments
    print(f"Matched segments" )
    for elem in common:
        print(f"{elem }" )
    #unmatched segments
    print(f"Unmatched segments" )
    for elem in unmatched:
        print(f"{elem }" )

if __name__ == '__main__':
    if len(sys.argv) <3:
        prog_name=sys.argv[0]
        usage="""{prog_name } will compare two stubb messages. before translation and after translation.
        This will show similar segments and missing segments
        {prog_name } <file_before_translation> <file_after_translation>
        """.foramt(prog_name, prog_name )

        print(usage )
        exit
    else:
        file1=sys.argv[1]
        file2=sys.argv[2]
        if os.path.isfile(file1 ) and os.path.isfile(file2 ):
            compare_messages(file1, file2 )
