import os
import sys
import glob
from win32com.client import DispatchEx
from pythoncom import CoInitialize, CoUninitialize
import win32com.client

if ( len(sys.argv) != 2):
    print("Usage: "+ sys.argv[0] +" <name_of_excel_file (xlsx)"  )
    print("This script will convert xlsx excel file to cvs file")
    print("and keeps the same name with .csv extension")
    exit(0) 

xlsx_file=sys.argv[1]
xlfiles=glob.glob("*" + xlsx_file + "*")
for xlfile in xlfiles:
    win32com.client.gencache.is_readonly=False
    cwd=os.getcwd() 

    xls_file=xlfile
    csv_file = os.path.join(cwd, xls_file[:-4]+'csv')
    print(csv_file) 
    xls_file=os.path.join(cwd, xls_file)
    print(xls_file) 
    # Open and setup Excel  
    CoInitialize()
    # DispatchEx opens a new Excel process
    xl_app = DispatchEx('Excel.Application')
    xl_app.Visible = 0
    xl_app.Workbooks.Open(xls_file)
    #xl_app.ActiveWorkbook.Notify = False
    # save as csv
    xl_app.ActiveWorkbook.SaveAs(csv_file, 0x6)
    #Save and close Excel
    xl_app.ActiveWorkbook.Close(SaveChanges=1)
    xl_app.Quit()
    CoUninitialize()

