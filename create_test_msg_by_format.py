#!c:/python39/python.exe
import sys
import os
from datetime import datetime
import re

def read_lines(filename ):
    inputlines=[]
    with open(filename) as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue
            inputlines.append(line)
    return inputlines

def three_word(words, idx,output, repeat_count ):
    if len(words) == 3:
        if words[0] == "[": 
            print(f"{words[1]}|{idx}" )
            output.append( f"{words[1]}|{idx}" )
            idx+=1
        elif words[0] == "{":
            for n in range(0,repeat_count ):
                print(f"{words[1]}|{idx}" )
                output.append( f"{words[1]}|{idx}" )
                idx+=1
        elif words[0] == "[{":
            for n in range(0,repeat_count ):
                print(f"{words[1]}|{idx}" )
                output.append(f"{words[1]}|{idx}" )
                idx+=1
 

    return (idx, output)

def one_word(words, idx,output, repeat_count) :
    words="".join(words)
    match=re.match("(\w+)|\[([a-z|A-Z].*?|[0-9])\]|\[{([a-z|A-Z].*?)}\]|{([a-z|A-Z].*?)}", words )

    if match:
        if match.group(1) is not None:
            print(f"{match.group(1)}|{idx}" )
            output.append(f"{match.group(1)}|{idx}" )
            idx+=1
        elif match.group(2) is not None:
            print(f"{match.group(2)}|{idx}" )
            output.append(f"{match.group(2)}|{idx}" )
            idx+=1
        elif match.group(3) is not None:
            for i in range(0, repeat_count ):
                print(f"{match.group(3)}|{idx}" )
                output.append(f"{match.group(3)}|{idx}" )
                idx+=1
        else:
            for i in range(0, repeat_count ):
                print(f"{match.group(4)}|{idx}" )
                output.append(f"{match.group(4)}|{idx}" )
                idx+=1


            
    return (idx,output)

def five_words(words, idx,output, repeat_count ):
    if len(words) == 5 and words[1] == "{":
        for i in range(0,repeat_count,1):
            print(f"{words[2]}|{idx}" )
            output.append(f"{words[2]}|{idx}" )
            idx+=1
    if len(words) == 5 and words[1] == "[":
        for i in range(0,repeat_count,1):
            print(f"{words[2]}|{idx}" )
            output.append(f"{words[2]}|{idx}" )
            idx+=1

    return (idx , output)

def repeat_msg(lines, idx, output,repeat_count):
    for n in range(0,repeat_count ):
        for line in lines:
            words=line.split()
            if len(words ) == 1:
                idx,output = one_word(words, idx,output,repeat_count) 
            elif len(words ) == 3:
                idx,output = three_word(words,idx,output,repeat_count )
            else:
                idx,output = five_words(words, idx,output,repeat_count )
    return (idx, output)
    

def create_msg(inputlines, output, repeat_count):
    line_count=0
    idx=1
    done1=0
    done2=0
    done3=0
    in_repeat = 0
    repeat=0
    repeats =[]
    msg_type=""
    event_type=""
    version=""
    previous_repeat=0
    inner_repeat1=[]
    inner_repeat2=[]
    inner_repeat3=[]

    while line_count < len(inputlines):
        line=inputlines[line_count ]
        if line_count < 8:
            if line.startswith("hl7vers:"):
                version=line.split()[1]
            elif line.startswith("name:"):
                event_type=line.split()[1]
                event_type="^".join(event_type.split("_"))
                msg_type=event_type.split("^")[0]
            line_count+= 1
            continue
        words=line.split()
        if words[0] == "MSH":
            print(f"MSH|^~\&|EPIC|{msg_type}|SMS|{msg_type}|199912271408|HARRIS|{event_type}|1817457|D|{version }|")
            output.append(f"MSH|^~\&|EPIC|{msg_type}|SMS|{msg_type}|199912271408|HARRIS|{event_type}|1817457|D|{version }|")
            idx+=1
            line_count+=1
            continue

        if line == "[ {" or line == "[{":
            in_repeat = 1
            done2=done1
            done3=done2 -1
            done1+=1


        elif line == "} ]" or line == "}]":
            done1-=1
            done2=done1-1
            done3=done2-1

        if line == "{":
            in_repeat = 1
            done2=done1
            done3=done2 -1
            done1+=1 
        elif line == "}":
            done1 -=1
            done2=done1 -1
            done3=done3 -1

        if in_repeat == 1 and done1 == 1:
            repeats.append(line)
            if len(inner_repeat1 )> 0:
                for i in range(0,repeat_count ):
                    for elem in inner_repeat1:
                        repeats.append(elem )
            inner_repeat1=[]

        if in_repeat == 1 and done2 == 1:
            inner_repeat1.append(line)
            if len(inner_repeat2 ) > 0:
                for i in range(0,repeat_count):
                    for elem in inner_repeat2:
                       inner_repeat1.append(elem )
                inner_repeat2=[]
            
        if in_repeat == 1 and done3 == 1:
            inner_repeat2.append(line )


        if in_repeat == 1 and done1 == 0:
            idx, output=repeat_msg(repeats, idx,output,repeat_count )
            repeats=[]
            in_repeat = 0
            
            
        if in_repeat == 0 :
            if len(words )==1:
                idx,output = one_word(words, idx,output,repeat_count) 
            elif len(words ) == 3:
                idx,output = three_word(words,idx,output, repeat_count )
            else:
                idx,output = five_words(words, idx,output, repeat_count )


        line_count+=1

    return output
if __name__ == "__main__":
    filename=""
    if len(sys.argv ) < 2:
        print(""" Please provide message type format
             example: {sys.argv[0 ] } <path_to_msg_format/DFT_P03>
             reapeat_count will be set to three as default
             example: {sys.argv[0]} </path_to_msg_format/DFT_P03> repeat_count""")
        exit(0 )
    elif len(sys.argv)== 3:
        filename=sys.argv[1]
        repeat_count=int(sys.argv[2])
    else:
        filename=sys.argv[1]
        repeat_count = 3

    if not os.path.exists(filename ):
        print(f"{filename } file does not exist")
        exit(0 )
    now = datetime.now()
    date_time=now.strftime("%Y%m%dT%H%M%S" )
    output = []
    inputlines = read_lines(filename )
    output = create_msg(inputlines, output, repeat_count)
    msg = "\r".join(output)
    for line in inputlines:
        if line.startswith("hl7vers" ):
            version =line.split()[1]
            break
    basename=os.path.basename(filename )
    outfile=f"{basename}_{version}_msg_{repeat_count}_repeat_{date_time}.txt"
    fh = open(outfile, 'w' )
    fh.write(msg )
    print(f"Created a message file name {outfile } in the current directory" )
    fh.close()
