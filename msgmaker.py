#!c:/python39/python
import os.path
import sys
import glob
import re

usage="""
    it needs a stubb message

"""
def read_stub(stubname):
    seg_order = []
    if os.path.exists(stubname ):
        with open(stubname )as fh:
            for line in fh:
                line=line.strip()
                if line == "":
                    continue
                segment=line.split("|")[0]
                seg_order.append(segment )
    else:
        print(f"stub file {stubname } does not exist" )

    return seg_order
    
def read_field_data(site,version):
    fields = {}
    hciroot=os.environ['HCIROOT']
    root_files=glob.glob(os.path.join(hciroot, "formats", "hl7", version,"fields"))

    site_files=glob.glob(os.path.join(hciroot, site, "formats", "hl7",version, "*", "fields"))
    root_files.extend(site_files )

    
    for file in root_files:
        with open(file ) as fh:
            for line in fh:
                match =re.match("{ITEM\s(\d+)}.*LEN.*?([-|' ']\d+).*?TYPE.*?(.*?)}",   line )
                if match:
                    item_id = match.group(1)
                    length = match.group(2)
                    fld_type=match.group(3).strip()
                    if not item_id in fields.keys():
                        fields[item_id ] = [length, fld_type ]
    return fields

def get_data_types(site,version):
    data_types={}
    hciroot=os.environ['HCIROOT']
    root_path=os.path.join(hciroot, "formats", "hl7", version,"datatypes")

    site_path=os.path.join(hciroot, site, "formats", "hl7",version, "datatypes") 
    root_file=glob.glob(root_path )
    site_file= glob.glob(site_path )
    for f in site_file:
        if f != "":
            root_file.append(f )
    data_type=""
    for file in root_file:
        with open(file) as fh:
            for line in fh:
                line=line.strip()
                match = re.match(".*?TYPE (.*?)}",line )
                if match:
                    data_type = match.group(1)
                    fields = re.split('{|}', line )
                    fields1 = list(filter(None, fields ) )
                    field="^".join([f for f in fields1 if f != ' ' ][4: ])
                    data_types[data_type ]= field


    return data_types


def read_seg_field_id(site, segments,seg_order):
    version = segments["version"]
    hciroot=os.environ['HCIROOT']
    root_path=os.path.join(hciroot, "formats", "hl7", version,"segments")

    site_path=os.path.join(hciroot, site, "formats", "hl7",version, "segments") 

    root_seg_files = glob.glob( root_path +os.sep + "*")
    site_seg_files = glob.glob(site_path +os.sep + "*" )  

    root_seg_files.extend(site_seg_files )
    seg_name=""
    item_id = ""
    for file in root_seg_files:
        with open(file ) as fh:
            for line in fh:
                line=line.strip()
                if line == "":
                    continue
                if line.startswith("name:" ):
                    seg_name=line.split()[1]
                match =re.match("{ITEM\s(.*?)}.*?{REQD.*?(\d+)}", line )
                if match:
                    item_id = match.group(1)
                    required=match.group(2) 
                    value=[item_id, required ]
                    if seg_name in seg_order:
                        if seg_name in segments.keys():
                            segments[seg_name].append(value) 
                        else:
                            segments[seg_name ]= [value]
    return segments 

if __name__ =="__main__":
    
    if len(sys.argv) < 2:
        print(usage)
        exit(0 )
    else:
        version=""
        msg_type=""
        event_type=""
        stubfilename=sys.argv[1]
        if os.path.exists(stubfilename ):
            with open(stubfilename ) as fh:
                for line in fh:
                    if line.startswith("MSH") :
                        words = line.split("|")
                        version = words[11]
                        msg_type,event_type = words[8].split("^")
                        break
        seg_order = read_stub(stubfilename )
        msg_type,event_type,vers=stubfilename.split("_")[0:3] 
        segments ={}
        segments["version"]=version
        segments["msg_type"]=msg_type
        segments["event_type"]=event_type

        site="icc_main_repo"

        segments = read_seg_field_id(site, segments,seg_order ) 

        fields = read_field_data(site,version )
        
        datatypes = get_data_types(site, version )
        msg=[]
        segment=""
        output = open(f"msg_{stubfilename}", "w" )
        for seg in seg_order:
            flds = segments[seg ] 
            length=len(flds )
            print(f"{seg }" )
            if seg == 'MSH':
                msg.append( f"MSH|^~\&|EPIC|PPR|SMS|PPR|199912271408|HARRIS|{msg_type}^{event_type}|1817457|D|{vers }")
                continue
            else:
                segment =f"{seg}|"

            for fld in flds:
                required=fld[1]
                fld_id=fld[0]
                fld_len, datatype = fields[fld_id ] 
                field_items=datatypes[datatype ]
                numFlds = len( datatypes[fields[fld[0] ][1]].split("^" ))
                if required == "1":
                    segment = segment + f"R-{datatype}|"
                else:
                    segment = segment +datatype+"|"
            msg.append(segment  )
        msg="\r".join(msg )
        print(msg )
        output.write(msg )
        output.close()
