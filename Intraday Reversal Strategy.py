# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 13:15:40 2018

@author: Alex
"""

from __future__ import division
import pandas as pd
import numpy as np
import itertools
from datetime import datetime

def dataprocessing():
    #清洗原始数据
    data = pd.read_excel('D:\quantOverALL\data\HS300 DATA.xls',skiprows=[0])
    codes = [list(data.columns)[4*i+1] for i in range(int(len(list(data.columns))/4)+1)]
    dates = list(data.iloc[2:,0])
    content=[]
    subcolumns1 = []
    subcolumns2 = [] 
    for code,i in itertools.izip(codes,range(len(codes))):
        priceOpen = list(data.iloc[2:,4*i+1])
        priceClose = list(data.iloc[2:,4*i+2])
        content.append(priceOpen)
        content.append(priceClose)
        subcolumns1.append(code)
        subcolumns1.append(code)
        subcolumns2.append('Open')
        subcolumns2.append('Close')    
    multicolumns=[subcolumns1,subcolumns2]
    content = np.array(content).T
    Data = pd.DataFrame(content,index = dates,columns=multicolumns)
    return Data

class context(object):
    def __init__(self):
        self.hold = []
        #用于记录持仓股票代码
        self.tempdict = {}
        #用于查找持仓股票对应订单号
        self.dict = {}
        #用于查看历史每支股票的订单
        self.log = []
        #用于储存所有订单信息
        self.total = 0
        #计数总共下过的订单
        self.startdate = None
        #记录开始时间
        self.timedict = {}
        #记录每个交易日的订单编号

def beforeTrading():
    #开盘前操作，该策略中无需操作
    pass

    
def on_Bars():
    global context
    #交易时间操作
    #首先更新数据
    date = context.date
    context.fired = False
    dayData = data.ix[date]
    dayOpen = dayData[:,'Open']
    #先进行平仓交易
    if context.hold != []:
        for code in context.hold:
            for order in context.tempdict[code]:
                price = dayOpen[code]
                context.log[order].closePosition(priceOut=price)
                #按开盘价进行平仓
        context.hold=[]
        context.tempdict={}
        #把持仓信息更新掉
    #再进行尾盘的筛选、购入操作
    dayClose = dayData[:,'Close']
    dayRet = (dayClose-dayOpen)/dayOpen
    dayRet.sort()
    trdList = list(dayRet[:10].index)
    #生成购买目标列表
    for code in trdList:
        #逐个创建订单，并更新持仓信息
        number = context.total
        context.total = context.total + 1
        price = dayClose[code]
        orderShares(code,number,date,price)
            
def orderShares(code,number,date,price,volume=100):
    global context      
    order = orders(code,number,date,price,volume)
    context.log.append(order)
    try:
        context.tempdict[code].append(number)
    except:
        context.tempdict[code] = [number]  
    try:
        context.dict[code].append(number)
    except:
        context.dict[code] = [number]        
    if code not in context.hold:
        context.hold.append(code)
    try:
        context.timedict[date].append(number)
    except:
        context.timedict[date] = [number]
def sellShares(code):
    pass

class orders():
    def __init__(self,code,number,date,price,volume=100):
        self.No = number
        self.code = code
        self.buyDate = date
        self.priceIn = price
        self.initVolume = volume
        self.volume = volume
        self.cost = volume*price
        self.revenue = 0
        self.ret = 0
    def closePosition(self,priceOut):
        self.priceOut = priceOut
        self.revenue = self.revenue + self.volume*priceOut
        self.volume = 0
        self.ret = (self.revenue-self.cost)/self.cost
    def sell_volume(self,volumeout):
        pass
    def sell_targert(self,target):
        pass
    def sell_position(self,position):
        pass

if __name__ == '__main__':
    data = dataprocessing()
    print '数据加载完毕！'
    dates = list(data.index)
    print '开始运行策略....'
    context = context()
    context.dates = dates
    context.data = data
    for date in dates[1:-2]:
        if context.startdate == None:
            context.startdate = date
        context.date = date
        beforeTrading()
        on_Bars()
    del date
    
        
        

    
