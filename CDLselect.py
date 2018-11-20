# -*- coding: utf-8 -*-
"""
Created on Wed Feb 07 11:00:31 2018

@author: Alex
"""

#根据Talib均线形态信号进行判断
'''请先安装TAlib'''

import numpy
import pandas
import talib as ta

'''CDLselect是一个数据装载器。
①启动时设置默认的选股范围，之后可以通过set_range手动设置选股范围
②通过load函数装载数据，装载的数据为加权后未经其它处理的数据
③通过processing函数将装载的数据按日聚合，成为日k线四维数据
④通过Patterndiagnose函数，根据日军k线数据，计算出涨跌信号，信号结果储存在PatternResult变量中'''

class CDLselect:
    def __init__(self):
        self.set_range()
        self.raw_data = {}
        print 'this one is for data processing & selecting stocks using CDL features'
    def set_range(self,T='D',stockList=[]):
        self.stockList = stockList
    def load_data(self):
        for stock in self.stockList:
            tmp = pandas.read_csv('D:\quantOverALL\weighted\\'+str(stock)+'+weighted.csv')
            self.raw_data[stock] = tmp
     #   self.datelist = set(self.raw_data[0].date)
    def dataProcessing(self,t='D'):
        #按照t的指定间隔进行均线数据聚合
        if t not in ('D','W','M'):
            print '错误的聚合间隔！'
        else:
            self.data={}
            if t == 'D':
                #按照天进行聚合
                for stock,raw_data in self.raw_data:
                    datelist=[]
                    seqlist =[]
                    openlist=[]
                    highlist=[]
                    lowlist =[]
                    closelist=[]
                    volumelist=[]
                    amountlist=[]
                    count = 1
                    datelist = list(raw_data.date.drop_duplicates())
                    for date in datelist:
                        seqlist.append(count)
                        count += 1
                        dayData = raw_data[raw_data.date == date]
                        open,high,low,close,volume,amount = (dayData.open.iloc[0],
                                                             max(dayData.high),
                                                             min(dayData.low),
                                                             dayData.close.iloc[-1],
                                                             sum(dayData.volume)*48/len(dayData),
                                                             sum(dayData.amount)*48/len(dayData))
                        openlist.append(open)
                        highlist.append(high)
                        lowlist.append(low)
                        closelist.append(close)
                        volumelist.append(volume)
                        amountlist.append(amount)
                    self.data[stock]=pandas.DataFrame({'seqNo':seqlist,'date':datelist,
                                                       'open':openlist,'high':highlist,
                                                       'low':lowlist,'close':closelist,
                                                       'volume':volumelist,'amount':amountlist},
                                                        columns=['seqNo','date','open','high','low',
                                                                 'close','volume','amount'])
            elif t == 'W':
                pass
    def CDL_PatternDiagnose(self):
        #检测k线形态
        #创建均线形态函数名列表
        list1=['ta.CDL3STARSINSOUTH','ta.CDL3WHITESOLDIERS','ta.CDLCONCEALBABYSWALL',
                    'ta.CDLHAMMER','ta.CDLHOMINGPIGEON','ta.CDLINVERTEDHAMMER','ta.CDLLADDERBOTTOM',
                    'ta.CDLMATCHINGLOW','ta.CDLMORNINGDOJISTAR','ta.CDLMORNINGSTAR'
                    ,'ta.CDLPIERCING','ta.CDLTAKURI','ta.CDLTASUKIGAP','ta.CDLUNIQUE3RIVER']
        list2=['ta.CDL2CROWS','ta.CDL3BLACKCROWS','ta.CDL3LINESTRIKE','ta.CDLADVANCEBLOCK',
                      'ta.CDLBREAKAWAY','ta.CDLDARKCLOUDCOVER','ta.CDLEVENINGDOJISTAR','ta.CDLEVENINGSTAR',
                      'ta.CDLHANGINGMAN','ta.CDLIDENTICAL3CROWS','ta.CDLINNECK','ta.CDLONNECK',
                      'ta.CDLSHOOTINGSTAR','ta.CDLSTALLEDPATTERN','ta.CDLTHRUSTING',
                      'ta.CDLUPSIDEGAP2CROWS']
        funcNameList = list1 + list2
        self.Patternresult={}
        for stock in self.stockList:
            #检验个股
            #初始化
            oneStockResult = []
            data = self.data[self.stockList.index(stock)]
            for func in funcNameList:
                func = eval(func)
                result = func(data.open.values,data.high.values,data.low.values,data.close.values)
                oneStockResult.append(result)    
            self.Patternresult[stock] = pandas.Series(sum(oneStockResult),index=data.date)
    def testWinRate(self):
        self.testResult={}
        for stock,signals in self.Patternresult:
            data = self.data[self.stockList.index(stock)]

#主程序以04和06两支股票进行了测试
if __name__ == '__main__':
    demo = CDLselect()
    #创建对象
    demo.set_range(stockList=['000004','000006','000063','000069'])
    demo.load_data()
    #加载数据，默认为000006,000004
    print '数据加载完成！'
    demo.dataProcessing()
    print '数据按日聚合完成！'
    demo.CDL_PatternDiagnose()
    print '均线形态判断完成！'
    
#结果：通过demo.Patternresult查看结果，0表示没有信号，正表示上涨信号，负表示下跌信号，
#绝对值大小表示强度，据人肉测试，出现信号，很可能在接下来2-3个交易日内出现对应波动，但是
#出现信号的第二个交易日往往不符合信号。说明信号有时滞性。
    
    
     
    
        
