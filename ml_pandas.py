#!c:\python38\python.exe

print("Hello World" ) 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data1 = {'key': ['K0', 'K1','K2', 'K3'],
        'Name': ['Mercy', 'Prince', 'John', 'Cena' ],
        'Address': ['Canada', 'Australia','India', 'Japan'],
        'Age': [27,24, 22,32] } 
data2 = {'key': ['K0', 'K1','K2', 'K3'],
        'Address': ['Canada', 'Uk','India', 'USA'],
        'Qualification':['BTech', 'BA', 'MS', 'PhD'] } 

df1 = pd.DataFrame(data1) 

df2 = pd.DataFrame(data2) 
print(df1.head() ) 
print("\n" ) 
print(df2.head()  ) 

res = pd.merge(df1, df2, on='key') 
print(res) 

res = pd.merge(df1, df2, on=['key', 'Address'] ) 
print(res) 


print("Left merge" )     
res = pd.merge(df1,df2,how='left', on=['key', 'Address'] ) 
print(res) 

print("Right merge" )     
res = pd.merge(df1,df2,how='right', on=['key', 'Address'] ) 
print(res) 


print("outer merge" )     
res = pd.merge(df1,df2,how='outer', on=['key', 'Address'] ) 
print(res) 

print("innner merge" )     
res = pd.merge(df1,df2,how='inner', on=['key', 'Address'] ) 
print(res) 

print("Join" ) 
data3 = { 'Name' : ['Mercy', 'Prince', 'John', 'Cena'], 'Age':[27,24,22,32]  } 
data4 = {'Address': ['Canada', 'UK', 'India', 'USA'], 'Qualification': ['BTech', 'BA', 'MS', 'PhD']  }  
df3=pd.DataFrame(data3) 
df4 = pd.DataFrame(data4) 
res = df3.join(df4) 
print(res) 


print("Inner join" ) 
res = df3.join(df4, how='inner') 
print(res) 

print("concat data" ) 
frames = [df3, df4] 
res = pd.concat(frames) 
print(res) 

print("concat -- ignore index" ) 
res = pd.concat(frames, ignore_index=True) 
print(res) 

print("concat --ignore_index and add as columns" ) 
res = pd.concat(frames, axis=1, ignore_index = True) 
print(res) 

print("append data" ) 
res = df3.append(df4) 
print(res) 

print("Generating random datetime" ) 

date = pd.date_range('10/28/2011', periods=8,freq='H' ) 

print(date) 

print("Generate datetime using range" ) 

date = pd.date_range(start='9/28/2018', end='10/28/2018', periods=10 ) 
print(date) 

print("Plotting line plot" ) 

df = pd.DataFrame(np.random.randn(10,4), index =pd.date_range('10/28/2020', periods=10), columns=list('ABCD')   ) 
df.plot() 
plt.show() 
print("bar graph" ) 

df = pd.DataFrame(np.random.rand(10,4), columns=['a','b','c','d']  ) 
df.plot.bar() 
plt.show() 
df.plot.bar(stacked=True) 
plt.show() 

print("plot histograph" ) 

df = pd.DataFrame({'A':np.random.randn(100)-3,
                    'B':np.random.randn(100)+1,
                    'C':np.random.randn(100)+3,
                    'D':np.random.randn(100)-1 },
                    columns={'A','B','C','D'} ) 
df.plot.hist(bins=20)  
plt.show() 

print("Scatter plot" ) 
df.plot.scatter(x='A', y='B') 
plt.show() 
    
