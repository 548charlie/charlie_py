#!c:/python310/python.exe
import os
import sys

def read_lines(filename):
    lines=[]
    if os.path.isfile(filename ):
        with open(filename ) as fh:
            for line in fh:
                line=line.strip()
                lines.append(line)         
    msg="\r".join(lines)
    return msg



if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename=sys.argv[1] 
        if os.path.isfile(filename ):
            file, ext = os.path.splitext(os.path.basename(filename))
            output=f"{file}_msg.hl7"
            msg= read_lines(filename)
            ofh=open(output, "w" )
            ofh.write(msg)
            ofh.close()
            print(f"Please see {output} for message" )
    else:
        print("""This {} will take a file with newline between segments and converts into HL7 message with \\r as segment separator\n
             usage: {} <name of the file>""".format(sys.argv[0], sys.argv[0] ))
