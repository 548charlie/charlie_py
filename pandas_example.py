#!c:/python38/python.exe
import pandas as pd
print("Hello World" ) 

df=pd.read_csv('temporal.csv') 
head=df.head(10) 
print(head) 
des =df.describe() 
print(des) 
info = df.info() 
print(info) 
from pandas_profiling import ProfileReport
prof = ProfileReport(df)
prof.to_file(output_file='pandas_report.html') 
