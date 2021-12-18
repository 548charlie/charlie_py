#!c:/python39/python.exe
import os
import sys

def read_lines(filename):
    msg=[]
    if os.path.isfile(filename ):
        with open(filename ) as fh:
            for line in fh:
                lines=line.split('\r' )
                msg.extend(lines ) 

    return msg



if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename=sys.argv[1] 
        output=f"seg_{filename}"
        lines= read_lines(filename)
        ofh=open(output, "w" )
        for line in lines:
            ofh.write(line)
        ofh.close()
        print(f"Please see {output} file with lines with segments" )

