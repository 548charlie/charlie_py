#!/opt/bin/python3.7

import pymysql
#from mysql.connector import errorcode
import datetime
import time
import subprocess
#import paramiko
from pathlib import Path
import base64
import os
import re
import csv
from shutil import move
import logging
from logging.handlers import TimedRotatingFileHandler
"""
within this quote is not used. It is here for my information.
import base64

with open("yourfile.ext", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
username="intfaandi"
password = "3a3hWSlRdHlANI"
server="TCFMDBD03"
database ="redcapdev2"
"""
lql_map = {} 
def get_date(data="",format="YYYYMMDDHHMMSS"):
    dstr = ""
    if data == "":
        d = datetime.datetime.now()  
        dstr = d.strftime("%Y%m%d%H%M%S")
    if format == "YYYYMMDD":
        datea = data.split("-") 
        if len(datea) == 3:
            (year, month,day)=datea
        else:
            (year, month,day) =(1900,1,1) 
        d = datetime.date(int(year), int(month), int(day))
        dstr = d.strftime("%Y%m%d") 
    elif format == "MMDDYYYY":
        datea = data.split("-") 
        if len(datea) == 3:
            (year,month,day)= datea
        else:
            (year,month,day)=(1900,1,1) 
        d = datetime.date(int(year), int(month),int(day)) 
        dstr = d.strftime("%m/%d/%Y") 
    if data == "msgid":
        d =datetime.datetime.now()
        dstr = d.strftime("%Y%m%d%H%M%S%f")  
    if data == "db_date":
       d = datetime.datetime.now()  
       dstr = d.strftime("%Y-%m-%d %H:%M") 
    return dstr 
        

def create_msg(msg_info, msg_info_printed):
    logger = logging.getLogger(__name__) 
    logger.info("Started creating message") 
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
    for key, value in msg_info.items():
        print(f" create msg key '{key}' value '{value}'  " ) 
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
    
    # insert some error checking here in case redcap has missing fields.
    
    if "patient_last_name" not in msg_info:
        msg_info["patient_last_name"][0]  = "pt_last_name_missing_in_redcap"
    if "patient_first_name" not in msg_info:
        msg_info["patient_first_name"][0]  = "patient_first_name_missing_in_redcap"
    if "patient_dob" not in msg_info:
        msg_info["patient_dob"] = "19000101"
    if "patient_gender" not in msg_info:
        msg_info["patient_gender"][0]  = "patient_gender_missing_in_redcap"
    if "guardian_phone" not in msg_info:
        msg_info["guardian_phone"][0]  = "guardian_phone_missing_in_redcap"
    if "ref_provider_npi" not in msg_info:
        msg_info["ref_provider_npi"][0]  = "ref_provider_npi_missing_in_redcap"
    if "ref_provider_last_name" not in msg_info:
        msg_info["ref_provider_last_name"][0]  = "ref_provider_last_name_missing_in_redcap"        
    if "ref_provider_first_name" not in msg_info:
        msg_info["ref_provider_first_name"][0]  = "ref_provider_first_name_missing_in_redcap"
    if "epic_eap" not in msg_info:
        msg_info["epic_eap"][0]  = "epic_eap_missing_in_redcap"
    if "visit_needed_asap" not in msg_info:
        msg_info["visit_needed_asap"][0]  = "?"        

    if 'reason_for_consult_diab_onset' in msg_info:
        onsetdate = msg_info['reason_for_consult_diab_onset'][0]  
        onsetdate = get_date(onsetdate, "MMDDYYYY") 
        msg_info['reason_for_consult_diab_onset'][0]  = onsetdate

    msh = '|'.join(MSH)
    logger.debug(f"MSH Segment:{msh}") 
    message.append(msh) 
    PID[0]= "PID"
    PID[1] = "1" 
    PID[5] = msg_info["patient_last_name"][0]  +'^'+msg_info["patient_first_name"][0]
    PID[7] = get_date(msg_info["patient_dob"][0] , "YYYYMMDD" )
    PID[8] = msg_info["patient_gender"][0]   
    PID[13] =msg_info["guardian_phone"][0] 
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
    logger.debug(f"ORC Segment:{orc} ")
    message.append(orc) 

    OBR[0]="OBR"
    OBR[1]="1" 
    OBR[4] = msg_info["epic_eap"][0] +"^^EPIC EAP ID"
    OBR[6]=get_date()
    OBR[7]=get_date()  
    OBR[16]=  msg_info['ref_provider_npi'][0]  +'^'+msg_info['ref_provider_last_name'][0]  +'^'+msg_info['ref_provider_first_name'][0]  +'^^^^^^NPI^^^^NPI'
    if msg_info["visit_needed_asap"][0] == "Y": 
        OBR[27] = "^^^^^ASAP^^^^^^1" 
    else:
        OBR[27] = "^^^^^R^^^^^^1" 

    msg_info_printed["patient_last_name"] = "1"
    msg_info_printed["patient_first_name"] = "1"
    msg_info_printed["patient_middle_name"] = "1"
    msg_info_printed["patient_dob"] = "1"
    msg_info_printed["patient_gender"] = "1"
    msg_info_printed["guardian_phone"] = "1"
    msg_info_printed["ref_provider_npi"] = "1"
    msg_info_printed["ref_provider_last_name"] = "1"
    msg_info_printed["ref_provider_first_name"] = "1"
    msg_info_printed["visit_needed_asap"] = "1"
    msg_info_printed["epic_eap"] = "1"
    msg_info_printed["encode_files"] = "1"
    msg_info_printed["extract_complete"] = "1"
    msg_info_printed["record"] = "1"
    msg_info_printed["referral_complete"] = "1"
    msg_info_printed["attachments"] = "1"
    msg_info_printed["referral_complete"] = "1"
    msg_info_printed["status_complete"] = "1"
    msg_info_printed["user_id"] = "1"

    obr = '|'.join(OBR) 
    logger.debug(f"OBR Segment:{obr} ")
    message.append(obr) 
    NTEs = [] 
    nte_count = 1
    for key, values in msg_info.items():
        for val in values:
            # Tim Tracy added reason_other to the pipe-delimited list on 9/6/19
            if re.search("ref_provider|guardian|comments|project_id|record_id|reason_other|note_|_note", key, re.IGNORECASE):
                NTE[0]="NTE"
                NTE[1] = str(nte_count)
                length = len(key)
                NTE[3] = key + " "*(53 - length)  + val
                nte_count += 1
                nte = '|'.join(NTE)
                NTEs.append(nte)
                NTE[0]="NTE"
                NTE[1]=str(nte_count)
                NTE[3]= "-"*120
                nte_count += 1
                nte = '|'.join(NTE)
                NTEs.append(nte)
                msg_info_printed[key] = "1" 

    # Tim added this section to pre-process the obx values, so we can print the un-used fields in the OBR comments section
    #logger.debug(f"Starting Tim Loop")

    for key, values in msg_info.items():
        for val in values:
            lql_key1 = msg_info["project_id"][0] +"|" +key +"|"+val
            lql_key2 = msg_info["project_id"][0] +"|" +key +"|"+"MAP REDCAP VALUE"
            if lql_key1 in lql_map or lql_key2 in lql_map:
                msg_info_printed[key] = "1"
  
    # now add any unmapped fields to the comments section
    
    for key, values in msg_info.items():
        #logger.debug(f"===key is now {key} ")
        if msg_info_printed[key] == "0":
            for val in values:
                #logger.debug(f"===val is now {val} ")
                NTE[0] = "NTE"
                NTE[1] = str(nte_count)
                length = len(key)
                NTE[3] = key + " "*(53 - length)  + val
                nte_count += 1
                nte = '|'.join(NTE)
                NTEs.append(nte)
                NTE[0] = "NTE"
                NTE[1] = str(nte_count)
                NTE[3] = "-"*120
                nte_count += 1
                nte = '|'.join(NTE)
                NTEs.append(nte)
                msg_info_printed[key] = "1"
    # --------------------------------------------------

    for nte in NTEs:                           
        message.append(nte)
    logger.debug(f"OBR NTE -- {nte} ")

    # Tim added section for lql_key2, to be able to map the values directly from redcap in cases
    #           where "MAP REDCAP VALUE" is populated in the lql_map.csv file.
    obx_count = 1
    nte_count = 1
    NTEs = [] 
    for key, values in msg_info.items():
        for val in values:
            lql_key1 = msg_info["project_id"][0] +"|" +key +"|"+val
            lql_key2 = msg_info["project_id"][0] +"|" +key +"|"+"MAP REDCAP VALUE"
            if lql_key1 in lql_map:
                (obx3, obx5)= lql_map[lql_key1].split("|")
                logger.debug(f"============in obx loop, obx3 is {obx3} and obx5 is {obx5}")
                if obx3 != "":
                    OBX[0] ="OBX"
                    OBX[1] = str(obx_count)
                    OBX[2] = "ST" 
                    OBX[3] = obx3
                    OBX[5] = obx5
                    obx = "|".join(OBX)
                    message.append(obx) 
                    obx_count +=1
                else:
                    logger.debug(f"============in obx loop, obx3 is empty, so not creating an obx")
            elif lql_key2 in lql_map:
                (obx3, obx5)= lql_map[lql_key2].split("|")
                if obx3 != "":
                    OBX[0] ="OBX"
                    OBX[1] = str(obx_count)
                    OBX[2] = "ST" 
                    OBX[3] = obx3
                    OBX[5] = val
                    obx = "|".join(OBX)
                    message.append(obx) 
                    obx_count +=1 
                else:
                    logger.debug(f"============in obx loop, obx3 is empty, so not creating an obx")                                 
            else:
                logger.debug(f"=========in obx loop, neither lql_key1 nor lql_key2 was found in lql_map, so no obx was created")
                
            # Tim Tracy commented out the following section on 9/6/19
            #if re.search("comments|reason_other", key):
                #NTE[0]="NTE"
                #NTE[1] = str(nte_count)
                #NTE[3] = key +"~" + val
                #nte_count += 1
                #nte = '|'.join(NTE) 
                #NTEs.append(nte)     

    outfilename = msg_info['patient_last_name'][0] +'_'+ str(msg_info["project_id"][0] )+"_"+str(msg_info["record"][0] )+".hl7" 
    outfilename = "_".join(outfilename.split())
    outfilename = os.path.join(msg_info["dst_dir"], outfilename ) 

    fout = open(outfilename, "w")

    part_msg = "\r".join(message) 
    fout.write(part_msg) 
    fout.write("\r") 
    doc_id = 1
    for encode_file in msg_info["encode_files"]:
        OBX[0] = "OBX"
        OBX[1] =str(obx_count)
        obx_count += 1
        OBX[2] = "ED"

        # Tim Tracy set OBX3 to "External Referral Note" on 9/7/2019
        #OBX[3]="Outside Orders"
        OBX[3]="External Referral Note"
        
        OBX[4]= str(doc_id) 
        doc_id += 1
        logger.debug(f"encoding file:{encode_file} ") 
        encoded_string ="XRSRSDFDSFASDFSERSE"

        (path, filename)= os.path.split(encode_file) 
        (basename, ext) = os.path.splitext(filename) 
        if len(ext) > 0 :
            ext =ext[1:].lower() 
        with open(encode_file, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        OBX[5] = "Referral^TCH^"+ext+"^Base64^"+encoded_string.decode("utf8")  
        dst_file = os.path.join(path, "done", filename) 
        move(encode_file, dst_file ) 
        #outfile = "junk_" + str(count) + ".pdf"
        #f = open(outfile, "wb")
        #out_text = base64.b64decode(OBX[5].encode("utf8")    ) 
        #f.write(out_text )
        #f.close() 
        obx='|'.join(OBX)
        logger.debug("OBX Segment: created obx with encoded text")
        fout.write(obx) 
        fout.write("\r") 

        #message.append(obx) 
        
    # Tim commented out the following two lines on 9/8/19 to eliminate remaining OBX nte's
    #for nte in NTEs:
        #message.append(nte)
    """
    full_message = "\r".join(message) 
    outfilename = msg_info['patient_last_name'][0] +'_'+ str(msg_info["project_id"][0] )+"_"+str(msg_info["record"][0] )+".hl7" 
    outfilename = "_".join(outfilename.split())
    outfilename = os.path.join(msg_info["dst_dir"], outfilename ) 

    fout = open(outfilename, "w")
    fout.write(full_message) 
    """
    fout.write("\n") 
    fout.close() 
    return "ok"

def get_document(src_filename, dst_filename):
    logger = logging.getLogger(__name__)
    logger.info(f"Starting to get document from {src_filename} to {dst_filename}"  ) 
    fileinfo = Path(dst_filename) 
    if not fileinfo.exists(): 
        logger.debug(f"{dst_filename} does not exists. Need to fetch it ")  
        proc = subprocess.Popen(["scp", "dsdesai@tcfldev03:"+src_filename, dst_filename])
        stat = os.waitpid(proc.pid, 0) 
        logger.debug(f"scp pid {stat}" ) 
        finfo = Path(dst_filename) 
        if finfo.exists():
            logger.debug(f"fetched file {dst_filename} ok ") 
            return "ok"
        else:
            logger.debug(f"problem fetching file {dst_filename}" ) 
            return "not_ok"
        """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect("tcfldev03", username="dsdesai", password="Newtch1", autocommit=True)
        ftp_client = ssh_client.open_sftp()
        ftp_client.get(src_filename, dst_filename ) 
        ftp_client.close() 
        """
        finfo = Path(dst_filename) 
        if finfo.exists():
            return "ok"
        else:
            return "not_ok"

    else:
        logger.debug("file:{} exists".format(dst_filename)  ) 
        return "ok"

def query_db(config): 
    username = config["username"]  
    password = config["password"] 
    server = config["server"] 
    database = config["database"] 
    src_dir = config["src_dir"] 
    dst_dir = config["dst_dir"]
      
    # Tim Tracy added the following line on 9/3/2019
    allowed_projects = config["allowed_projects"] 

    logger = logging.getLogger(__name__) 
    logger.debug("started query_db") 
    try:
        cnx = pymysql.connect(user=username, password=password,
                                  host=server,
                                  database=database,
                                 connect_timeout=60)

        proj_cursor = cnx.cursor()
        
        # Tim Tracy added the condition regarding project_id IN...
                
        query1 = """SELECT distinct project_id, record, event_id
                FROM redcap_data rd1
                WHERE
                rd1.project_id IN ({})
                AND rd1.record IN
                (SELECT rd2.record
                FROM redcap_data rd2
                WHERE rd2.field_name = 'referral_complete'
                AND rd2.value = '2'
                AND rd2.project_id = rd1.project_id)
                AND ((rd1.field_name = 'extract_complete' AND rd1.value =0)
                OR (rd1.record NOT IN
                (SELECT rd4.record
                FROM redcap_data rd4
                WHERE rd4.field_name = 'extract_complete'
                AND rd4.project_id = rd1.project_id)))
                AND ((rd1.field_name = 'status_complete' AND rd1.value <> '2')
                OR (rd1.record NOT IN
                (SELECT rd3.record
                FROM redcap_data rd3
                WHERE rd3.field_name = 'status_complete'
                AND rd3.project_id = rd1.project_id))) """.format(allowed_projects)
                
        logger.debug("executed the query {}".format(query1)  ) 
        proj_cursor.execute(query1 ) 
        rows = proj_cursor.fetchall()
        logger.debug(f"There are {len(rows)} rows in database to process" ) 
        for project_id, record, event_id in rows:
          
            logger.debug("project Id: {}  and associated record:{} and event_id:{} ".format(project_id, record, event_id) )

            record_cursor = cnx.cursor() 

            data_query= """select TRIM(field_name),TRIM(value) 
                        from redcap_data
                        where project_ID={} and record={}""".format(project_id, record) 
            logger.debug("data query:{}".format(data_query)  ) 
            record_cursor.execute(data_query)   
            count = 1
            doc_ids = []
            
            info = {}
            info["dst_dir"] = dst_dir;
            info["project_id"] =[str(project_id)]
            info["record"] = [record]

            # Tim added this to track whether the field was utilized somewhere., "1" means it it was used            
            info_printed = {}
            info_printed["dst_dir"] = "1";
            info_printed["project_id"] = "1"
            info_printed["record"] = "0"
            
            rec_rows = record_cursor.fetchall() 
            logger.debug(f"There are {len(rec_rows)} rows to process" ) 
            
            del record_cursor
            for  field_name, value in rec_rows:
                
                logger.debug("record: {} field_name {} value {}".format(record, field_name, value )    )
                info_printed[field_name] = "0"
                if field_name in info: 
                    info[field_name].append(value)
                    
                else:
                    info[field_name] = [value] 

                #get list of attachments doc_ids
            for key, value in info.items() :
                logger.debug("key :{} value:{}".format(key, value)   )
                if key.find("attachment") >= 0:
                    for item in value:
                        if item.isnumeric():
                            doc_ids.append(item) 
                        logger.debug(f"doc_id to fetch :{item} ") 
            if len(doc_ids) == 0:
                docids = ""
            else:
                docids = ",".join(doc_ids) 

            logger.debug(f"docids {docids}")
            if docids != "":
                attachment_query = """select stored_name 
                                    from redcap_edocs_metadata 
                                    where doc_id in ({})""".format(docids)
                logger.debug("attachment_query :{}".format(attachment_query)  ) 
                doc_cursor = cnx.cursor() 
                doc_cursor.execute(attachment_query) 
                filenames =[] 
                file_rows = doc_cursor.fetchall() 
                del doc_cursor
                for filename in file_rows:
                    logger.debug(filename) 
                    org_file = filename[0] 
                    logger.debug(f'File name:{org_file}'  ) 
                    src_filename = os.path.join(src_dir, org_file) 
                    dst_filename = os.path.join(dst_dir, org_file) 
                    result =get_document(src_filename, dst_filename)             
                    if result == "ok":
                        filenames.append(dst_filename) 
                    else:
                        logger.error("file could not be fetched") 
                info["encode_files"] = filenames 
            else:
                info["encode_files"] = []  

            result = create_msg(info, info_printed )
             
            #write method to update the status
            if result == "ok":
                count_query = """select count(*) 
                    from redcap_data
                    where project_ID={}
                    and field_name="status_complete"
                    and record={}""".format(project_id, record)
                    
                logger.debug("count_query :{}".format(count_query)  ) 
                count_cursor = cnx.cursor() 
                count_cursor.execute(count_query) 
                count_rows = count_cursor.fetchall()
                logger.debug(f"There are {len(count_rows)} rows to process from the count_query" )
                del count_cursor
                for count_row in count_rows:
                    logger.debug(count_row) 
                    count_val = count_row[0] 
                    logger.debug(f'count query returned a value of:{count_val}'  )
                    
                    if count_val == 0:
                        insert_sql = """ insert INTO redcap_data
                                     (project_id,event_id,record,field_name,value)   
                                     values ({},{},{},'status_complete','2')""".format(project_id, event_id, record)

                        logger.debug(f"executed insert query:{insert_sql}"  ) 
                        insert_cursor = cnx.cursor()
                        affected_row = insert_cursor.execute(insert_sql) 
                        logger.debug(f"rows affected {affected_row}" ) 
                        cnx.commit() 
                        del insert_cursor                    
                    else:
                        update_sql = """ update redcap_data
                                     set value = 2
                                     where project_id = {} 
                                     and record = {}
                                     and field_name = "status_complete"
                                     """.format(project_id, record  )
                        logger.debug(f"executed update query:{update_sql}"  ) 
                        update_cursor = cnx.cursor()
                        affected_row = update_cursor.execute(update_sql) 
                        logger.debug(f"rows affected {affected_row}" ) 
                        cnx.commit() 
                        del update_cursor                    
                fcompTime_sql = """ select count(*)
                from redcap_data
                where project_id = {} 
                and record = {} 
                and field_name = "fcompletedtime" """.format(project_id, record) 
                logger.debug(f"get fcompletetime count query {fcompTime_sql}" ) 
                fcompTime_cur = cnx.cursor() 
                fcompTime_cur.execute(fcompTime_sql)  
                fcompTime_row = fcompTime_cur.fetchone() 
                fcompTime_count = fcompTime_row[0] 
                logger.debug(f"Number of rows of fcompleteTime: {fcompTime_count}" ) 
                del fcompTime_cur
                if fcompTime_count == 0:
                    dbdate = get_date("db_date") 
                    ins_stmt = """insert into redcap_data
                    (project_id, event_id,record, field_name, value) 
                    VALUES ({},{},{},'fcompletedtime','{}' )""".format(project_id, event_id, record, dbdate)  
                    logger.debug(f"insert stmt {ins_stmt}" ) 
                    ins_cur = cnx.cursor() 
                    ins_cur.execute(ins_stmt) 
                    cnx.commit() 
                    del ins_cur

                stnotes_sql = """ select count(*)
                from redcap_data
                where project_id = {} 
                and record = {} 
                and field_name = "status_notes" """.format(project_id, record) 
                logger.debug(f"get status notes count query {stnotes_sql}" ) 
                stnotes_cur = cnx.cursor() 
                stnotes_cur.execute(stnotes_sql)  
                stnotes_row = stnotes_cur.fetchone() 
                stnotes_count = stnotes_row[0] 
                logger.debug(f"Number of rows of status_notes: {stnotes_count}" ) 
                del stnotes_cur
                if stnotes_count == 0:
                    dbdate = get_date("db_date") 
                    ins_stmt = """insert into redcap_data
                    (project_id, event_id,record, field_name, value) 
                    VALUES ({},{},{},'status_notes', "This is inserted by interface on {}" )""".format(project_id, event_id, record, dbdate)  
                    logger.debug(f"insert stmt {ins_stmt}" ) 
                    ins_cur = cnx.cursor() 
                    ins_cur.execute(ins_stmt) 
                    cnx.commit() 
                    del ins_cur



                #result =get_document(src_filename, dst_filename)
                #info["encode_files"] = filenames 
                #params = [ project_id, record] 
                #update_status(cnx,params ) 

    except pymysql.Error as err:
        logger.debug(f"Something is wrong message {err}  ")
        logger.error(err, exc_info=True)
    else:
      cnx.close()
      logger.debug("Closed the db connection" )

def update_status(cnx, params):
    logger = logging.getLogger(__name__) 
    logger.debug("started update_status") 
    try:
        update_sql = """ update redcap_data
                        set value = 2
                        where project_id = {} 
                        and record = {}
                        and field_name = "status_complete"
                    """.format(params[0], params[1]  ) 
        logger.debug(f"executed update query:{update_sql}"  ) 
        update_cursor = cnx.cursor()
        affected_row =update_cursor.execute(update_sql) 
        cnx.commit() 
        del update_cursor
        logger.debug(f"number of rows affected {affected_row}" ) 
    except pymysql.Error as err:
        logger.debug(f"Something is wrong message {err}  ")
        logger.debug(err, exc_info=True)
    else:
      cnx.close()

    

def create_lql_map(filename):
    p = Path(filename)
    lql_map = {}  
    if p.exists():
        logger.debug(f"filename : {filename} exists" ) 
        line_count = 0
        with p.open(mode="r")  as csv_file:
            reader = csv.reader(csv_file,delimiter =",")
            for row in reader:
                #logger.debug(f"{line_count}:  {row} ")
                key = row[1].strip()  +"|"+row[4].strip() +"|"+row[5].strip()  # projectid|redcap_FIELD_NAME|redcap_Value
                value=row[6].strip()+"|" + row[9].strip() # OBX3|send_to_epic_as
                lql_map[key] = value 
    else:
        logger.debug(f"File named : {filename} does not exist" ) 

    #for key, value in lql_map.items():
    #logger.debug(f"key :{key} Value:{value}"  ) 
    
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
        
if __name__ == "__main__":
    cfg_file = "/data/scripts/referral_aix.cfg"
    config_items = {} 
    p = Path(cfg_file) 
    if p.exists() :
        with open(cfg_file, "r") as fh:
            for line in fh:
                line = line.strip() 
                if line.startswith("#") or line =="":
                    continue
                
                (key, value) = line.split("=")
                config_items[key.strip()] = value.strip().strip('\"') 

        """
        log_filename = "/data/dev/resource/referral/referral.log"
        src_dir = "/REDCap"
        dst_dir = "/data/dev/resource/referral"
        lql_filename ="/data/dev/resource/referral/epic_lql_map.csv"
        """
        log_filename = config_items["log_filename"] 
        logger = get_logger(log_filename) 
        src_dir = config_items["src_dir"] 
        dst_dir = config_items["dst_dir"] 
        lql_filename = config_items["lql_filename"] 
        lql_map = create_lql_map(lql_filename) 
        query_db(config_items) 
    else:
        print("Config file is missing. Please create config file and run it again") 
    prevDay = datetime.date.today()-datetime.timedelta(1) 
    crontab_log = config_items["crontab_log"] 
    preCronlogname=crontab_log +"_"+ str(prevDay)
    plfile = Path(preCronlogname) 
    lfile = Path(crontab_log) 
    if not plfile.exists():
        if lfile.exists():
            move(crontab_log, preCronlogname) 
    preLogfilename = log_filename +"_"+ str(prevDay) 
    rlfile = Path(preLogfilename) 
    rfile = Path(log_filename) 
    if not rlfile.exists():
        if rfile.exists():
            move(log_filename, preLogfilename) 
         
