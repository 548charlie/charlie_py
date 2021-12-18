#!c:/python37/python

import mysql.connector
from mysql.connector import errorcode
import datetime
import subprocess
import paramiko
from pathlib import Path
import base64
import os
import re
import csv
import logging
from logging.handlers import TimedRotatingFileHandler
import sys
"""
import base64

with open("yourfile.ext", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
"""
print("Hello World") 
username="intfaandi"
password = "3a3hWSlRdHlANI"
server="TCFMDBD03"
database ="redcapdev2"
lql_map = {} 
def get_date(data="",format="YYYYMMDDHHMMSS"):
    dstr = ""
    if data == "":
        d = datetime.datetime.now()  
        dstr = d.strftime("%Y%m%d%H%M%S")
    if format == "YYYYMMDD":
        (year, month,day)=data.split("-")  
        d = datetime.date(int(year), int(month), int(day))
        dstr = d.strftime("%Y%m%d") 
    if data == "msgid":
        d =datetime.datetime.now()
        dstr = d.strftime("%Y%m%d%H%M%S%f")  
    return dstr 
        

def create_msg(msg_info):
    logger = logging.getLogger(__name__)
    logger.info("started create message") 
    message = [] 
    MSH= []
    for i in range(15):
        MSH.append('')
    PID = []
    for i in range(25):
        PID.append('')
    PV1 =[]
    for i in range(30):
        PV1.append('')
    ORC=[]
    for i in range(20):
        ORC.append('')
    OBR=[]
    for i in range(30):
        OBR.append('')
    OBX=[]
    OBXs =[] 
    for i in range(15):
        OBX.append('')
    GT1=[]
    for i in range(30):
        GT1.append('')
    NTE = []
    for i in range(5):
        NTE.append('') 

    MSH[0]="MSH"
    MSH[1]='^~\\&'
    MSH[2] = "EPIC"
    MSH[3] ="EXT"
    MSH[4] ="EPIC"
    MSH[5]= "TCH"
    MSH[6] = get_date()  
    MSH[8] = "ORM^O01"
    MSH[9] = get_date("msgid")  
    MSH[10] = "D"
    MSH[11] = "2.3" 

    msh = '|'.join(MSH)
    logger.debug(f"MSH Segment:{msh} ") 
    message.append(msh) 
    PID[0]= "PID"
    PID[1] = "1" 
    PID[5] = msg_info["patient_last_name"][0]  +'^'+msg_info["patient_first_name"][0]    

    PID[7] = get_date(msg_info["patient_dob"][0] , "YYYYMMDD" )  
    PID[8] = msg_info["patient_gender"][0]   
    pid = '|'.join(PID)
    logger.debug(f"PID Segment:{pid} ") 
    message.append(pid) 
    PV1[0] = "PV1"
    PV1[7] = msg_info['ref_provider_npi'][0]  +'^'+msg_info['ref_provider_last_name'][0]  +'^'+msg_info['ref_provider_first_name'][0]  +'^^^^^^NPI^^^^NPI'
    pv1 = '|'.join(PV1)
    logger.debug(f"PV1 Segment:{pv1} ") 
    message.append(pv1) 


    ORC[0]="ORC"
    ORC[1] ="NW" 
    orc='|'.join(ORC)
    logger.debug(f"ORC Segment: {orc} ")
    message.append(orc) 

    OBR[0]="OBR"
    OBR[1]="1" 
    OBR[4] = "REF185^^EPIC EAP ID"
    OBR[6]=get_date()
    OBR[7]=get_date()  
    OBR[16]=  msg_info['ref_provider_npi'][0]  +'^'+msg_info['ref_provider_last_name'][0]  +'^'+msg_info['ref_provider_first_name'][0]  +'^^^^^^NPI^^^^NPI'
    OBR[27] = "^^^^^RU^^^^^1" 
    obr = '|'.join(OBR) 
    logger.debug(f"OBR Segment:{obr} ")
    message.append(obr) 
    NTEs = [] 
    nte_count = 1
    for key, values in msg_info.items():
        for val in values:
            if re.search("ref_provider|guardian|comments", key, re.IGNORECASE):
                NTE[0]="NTE"
                NTE[1] = str(nte_count)
                NTE[3] = key +"~" + val
                nte_count += 1
                nte = '|'.join(NTE) 
                NTEs.append(nte)  
    for nte in NTEs:
        message.append(nte)
    logger.debug(f"OBR NTEs {nte} ") 

    obx_count = 1
    nte_count = 1
    NTEs = [] 
    for key, values in msg_info.items():
        for val in values:
            lql_key = "RENAL REFERRAL - REF185|"+key +"|"+val
            if lql_key in lql_map:
                OBX[0] ="OBX"
                OBX[1] = str(obx_count)
                OBX[3] = lql_map[lql_key]
                OBX[5] = val.replace("_", " ") 
                obx = "|".join(OBX)
                message.append(obx) 
                obx_count +=1
            if re.search("comments|reason_other", key):
                NTE[0]="NTE"
                NTE[1] = str(nte_count)
                NTE[3] = key +"~" + val
                nte_count += 1
                nte = '|'.join(NTE) 
                NTEs.append(nte)     
    for encode_file in msg_info["encode_files"]:
        OBX[0] = "OBX"
        OBX[1] =str(count)
        count += 1
        logger.debug(f"encoding file:{encode_file}") 
        encoded_string ="XRSRSDFDSFASDFSERSE"
        with open(encode_file, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        OBX[5] = "Referral^TCH^PDF^Base64^"+encoded_string.decode("utf8")  
        #outfile = "junk_" + str(count) + ".pdf"
        #f = open(outfile, "wb")
        #out_text = base64.b64decode(OBX[5].encode("utf8")    ) 
        #f.write(out_text )
        #f.close() 
        obx='|'.join(OBX)
        logger.debug(f"OBX Segment:{obx} ") 
        message.append(obx) 

    for nte in NTEs:
        message.append(nte)

    full_message = "\r".join(message) 

    outfilename = msg_info['patient_last_name'][0] +'_'+ str(msg_info["project_id"][0] )+"_"+str(msg_info["record"][0] )+".hl7" 
    fout = open(outfilename, "w")
    fout.write(full_message) 
    fout.close() 

def get_document(src_filename, dst_filename):
    logger = logging.getLogger(__name__)
    logger.info(f"Getting document from {src_filename} to {dst_filename} "  ) 
    fileinfo = Path(dst_filename) 

    if not fileinfo.exists(): 
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect("tcfldev03", username="dsdesai", password="Newtch1")
        ftp_client = ssh_client.open_sftp()
        ftp_client.get(src_filename, dst_filename ) 
        ftp_client.close() 
        info["encode_files"] = dst_filename 
    else:
        logger.debug("file:{} exists".format(dst_filename)  ) 

def query_db(src_dir, dst_dir): 
    logger = logging.getLogger(__name__)
    logger.info("started processing database entries") 
    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                  host=server,
                                  database=database)


        proj_cursor = cnx.cursor(buffered=True)
        record_cursor = cnx.cursor(buffered=True) 
        query1 = """select project_id, record 
                from redcap_data
                where field_name="extract_complete" 
                and value=0 
                """
        logger.debug(query1)  
        proj_cursor.execute(query1 ) 
        for project_id, record in proj_cursor:
            logger.debug("project Id: {}  and associated record:{}  ".format(project_id, record) ) 

            data_query= """select TRIM(field_name),TRIM(value) 
                        from redcap_data
                        where project_ID={} and record={}""".format(project_id, record) 
            logger.debug("query:{}".format(data_query)  ) 
            record_cursor.execute(data_query)   
            count = 1
            doc_ids = [] 
            info = {} 
            info["project_id"] =[str(project_id)]
            info["record"] = [record] 
            for  field_name, value in record_cursor:
                
                #print("record: {} field_name {} value {}".format(record, field_name, value )    )
                if field_name in info: 
                    info[field_name].append(value) 
                    
                else:
                    info[field_name] = [value] 

                #get list of attachments doc_ids
            for key, value in info.items() :
                logger.debug("key :{} value:{}".format(key, value)   )
                if key.find("test_result_attachmen") >= 0:
                    doc_ids.append(value) 
            docids = ",".join(doc_ids) 
            if docids != "":
                attachment_query = """select stored_name 
                                    from redcap_edocs_metadata 
                                    where doc_id in ({})""".format(docids)
                logger.debug("attachment_query :{}".format(attachment_query)  ) 
                record_cursor.execute(attachment_query) 
                filenames =[] 
                for filename in record_cursor:
                    print(filename) 
                    org_file = filename[0] 
                    logger.debug(f'File name:{org_file}'  ) 
                    src_filename = os.path.join(src_dir, org_file) 
                    dst_filename = os.path.join(dst_dir, org_file) 
                    get_document(src_filename, dst_filename)             
                    filenames.append(dst_filename) 
                info["encode_files"] = filenames 
            else:
                info["encode_files"] = []  

            create_msg(info ) 
            #write method to update the status
            params = [ project_id, record] 
           # update_status(cnx,params ) 
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logger.error(f"Something is wrong with your user name or password{err} ", exc_info=true)
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logger.error(f"Database does not exist{err} ",exc_info=true)
      else:
        logger.error(err, exc_info=true)
    else:
      cnx.close()

def update_status(cnx, params):
    logger = logging.getLogger(__name__)
    logger.info(f"updating the status of the row  with parameters {params}"  ) 
    try:
        update_sql = """ update redcap_data
                        set value = 1
                        where project_id = {} 
                        and record_id = {}
                        and field_name = "extract_complete""".format(params[0], params[1]  ) 
        logger.debug(update_sql) 
        update_cursor = cnx.cursor(buffered=True)
        update_cursor.execute(update_sql) 

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logger.error(f"Something is wrong with your user name or password{err} ",exc_info=true)
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logger.error(f"Database does not exist {err} ", exc_info=true)
      else:
        logger.error(err)
    else:
      cnx.close()


def create_lql_map(filename):
    logger = logging.getLogger(__name__)
    logger.info("parsing %s", filename) 
    p = Path(filename)
    lql_map = {}  
    if p.exists():
        logger.debug(f"filename : {filename} exists" ) 
        line_count = 0
        with p.open(mode="r")  as csv_file:
            reader = csv.reader(csv_file,delimiter =",")
            for row in reader:
                logger.debug(f"{line_count}:  {row} ")
                key = row[1].strip()  +"|"+row[2].strip() +"|"+row[3].strip()  
                value=row[4].strip() 
                lql_map[key] = value 
    for key, value in lql_map.items():
        logger.debug(f"key :{key} Value:{value}"  ) 
    
    return lql_map
def get_logger(path):
    level = logging.DEBUG 
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter('%(asctime)s|%(filename)s|%(funcName)s|%(lineno)d|%(levelname)s|%(message)s','%m-%d %H:%M:%S')
    #formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
    logger.setLevel(level)
    handler = TimedRotatingFileHandler(path, when="d", interval=1,backupCount=30) 
    handler.setLevel(level)
    handler.setFormatter(formatter) 
    logger.addHandler(handler) 
    return logger    
def testing():
    logger = logging.getLogger(__name__)
    logger.info("This is is test") 
if __name__ == "__main__":
    log_file = "c:/dinakar/junk/referral.log"
    logger = get_logger(log_file) 

    src_dir = "/REDCap"
    dst_dir = "c:/dinakar/junk"
    logger.debug("src dir %s", src_dir)
    testing() 
    lql_filename ="c:/junk/epic_lql_map.csv"
    lql_map = create_lql_map(lql_filename) 

    query_db(src_dir, dst_dir) 

    junk = {'clin_doc_submission_type':'1',
    'extract_complete':'1',
    'guardian_first_name':'g1',
    'guardian_last_name':'gl',
    'guardian_phone':'(281) 302-6786',
    'guardian_phone_type':'0',
    'patient_dob':'1955-05-05',
    'patient_first_name':'five',
    'patient_gender':'1',
    'patient_last_name':'fivelast',
    'preferred_locations':'1',
    'reason_for_consultation':'10',
    'record_id':'5',
    'ref_provider_address':'t1',
    'ref_provider_city':'houston',
    'ref_provider_fax':'(281) 302-6786',
    'ref_provider_first_name':'d1',
    'ref_provider_last_name':'d2',
    'ref_provider_npi':'1234567890',
    'ref_provider_phone':'(281) 302-6786',
    'ref_provider_state':'43',
    'ref_provider_zip':'77030',
    'referral_complete':'2',
    'test_result_attachments':'68057',
    'testing_results':'1',
    'visit_needed_asap':'2'} 
     
