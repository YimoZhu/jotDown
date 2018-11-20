# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 13:30:51 2018

@author: AS
"""
import pandas as pd
import copy
data = pd.read_csv('000001+weighted.csv')
data=data.iloc[:,1:]
#调整顺序，使数据按照时间先后排列
data=data.sort_values(by="date" )
index=[-1]
for i in range(len(data)-1):
    if data.iloc[i,0]!=data.iloc[i+1,0]:
        index.append(i)
#print(index)
temp=pd.DataFrame(columns=['date','seqNo','open', 'high', 'low','close', 'volume','amount'])
for j in range(len(index)-1):
    temp=temp.append(data.iloc[index[j]+1:index[j+1]+1].sort_values(by='seqNo'))
    #print(temp)
temp=temp.append(data.iloc[index[-1]+1:].sort_values(by='seqNo'))
data=temp
data=data.reset_index(drop=True)  
#print(data)
data2=copy.deepcopy(data)

#线性插值
def interp(data,data2):
    num=0#已经插了num行
    if data.iloc[0,1]!=1:
        data.drop(data.iloc[0:48-data.iloc[0,1]+1],inplace=True)
    for row in data.iterrows():
        #print(row[0])
        if row[0]!=len(data)-1:
            if (row[1]['seqNo']!=48 or data.iloc[row[0]+1,1]!=1) and data.iloc[row[0]+1,0]!=row[1]['date']:
                #temp=pd.DataFrame(columns=['date','seqNo','open', 'close', 'high', 'low','volume','amount']) 
                add=data.iloc[row[0]+1,1]+47-row[1]['seqNo']
                above=row[1]
                below=data.iloc[row[0]+1]
            
                for i in range(int(add)):
                    insert=(below-above)/data.iloc[row[0]+1,1]*(i+1)+below
                    if i+row[1]['seqNo']>=48:
                        insert['date']=data.iloc[row[0]+1,0]
                        insert['seqNo']=i+row[1]['seqNo']-47
                    else:
                        insert['date']=row[1]['date']
                        insert['seqNo']=row[1]['seqNo']+i+1
                    #print(insert)
                    data2=pd.concat([data2.iloc[:row[0]+1+num+i].append(insert.to_frame(name=None).T),data2.iloc[row[0]+1+num+i:]],axis=0,ignore_index=True)
                num=num+int(add)
                data2=data2.reset_index(drop=True)  
                #print(row[0])               
    return data2
data2=interp(data,data2)
#print(len(data2))
data2.to_csv('new.csv')