import pandas as pd
import numpy as np

weight = pd.read_clipboard()
codes = list(weight.index)
for code in codes:
    data = pd.read_csv('D:\quantOverALL\data\\'+code[:-3]+'.csv')
    weights = weight.T[code]
    datelist=[]
    seqlist=[]
    openlist=[]
    highlist=[]
    lowlist=[]
    closelist=[]
    volumelist=[]
    amountlist=[]
    for row in data.iterrows():
        date = str(int(row[1]['date']))
        w = weights[date]
        seq = str(int(row[1]['seqNo']))
        datelist.append(date)
        seqlist.append(seq)
        openlist.append(row[1]['open']*w)
        closelist.append(row[1]['close']*w)
        highlist.append(row[1]['high']*w)
        lowlist.append(row[1]['low']*w)
        volumelist.append(row[1]['volume']*w)
        amountlist.append(row[1]['amount']*w)
    weighted = pd.DataFrame({'date':datelist,'seqNo':seqlist,'open':openlist,
                             'high':highlist,'low':lowlist,'close':closelist,
                             'volume':volumelist,'amount':amountlist},columns=['date',
                                'seqNo','open','high','low','close','volume','amount'])
    weighted.to_csv('D:\quantOverALL\weighted\\'+code[:-3]+'+weighted.csv')  
    