#!/usr/bin/python3
import os
import sys

def splitMsg_ro_fields(filename ):
    with open(filename ) as fh:
        for line in fh:
            line=line.strip()
            fldsep=line[3]
            cmpsep=line[4]
            segments=line.split('\r')
            for seg in segments:
                seg_name=seg[0:3]
                fields=seg.split(fldsep)
                for i, field in enumerate(fields ):
                    subfields=field.split('^')
                    for j,subfield in enumerate(subfields ):
                        print(f"{seg_name}_{i}_{j}{fldsep } {subfield }")





if __name__ == '__main__':
    if len(sys.argv) >1:
        filename = sys.argv[1]
        splitMsg_ro_fields(filename )
