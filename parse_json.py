#!/usr/bin/env python3
import sys, json
import os

def parse_json(filename ):
    print(f"{filename }" )
    with open(filename ) as fh:
        data=json.load(fh)
        def parse(data, root=""):
            for key, value in data.items():
                if isinstance(value, str  ):
                    if (key == "resourceType" ):
                        print(f"======={value}======" )
                    print(f"{root}->{key}| {value}")
                key=root+"->"+key
                if isinstance(value,dict ):
                    parse(value,key )
                elif isinstance(value, list ):
                    for val in value:
                        if isinstance(val, str ):
                            pass
                        elif isinstance(val, list ):
                            pass
                        else:
                            parse(val,key)
        parse(data)
if __name__ == '__main__':
    if len(sys.argv ) > 1  :
        filename = sys.argv[1]
        
        if os.path.isfile(filename ):
            parse_json(filename )
        else:
            print(f"File {filename } does not exist" )
