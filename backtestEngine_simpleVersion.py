# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 18:56:56 2018

@author: Alex
"""
from __future__ import division
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib as mpl

class result(object):
    pass

class BacktestEngine_simpleVersion():
    def __init__(self,context):
        self.context = context
        self.tradedates = []
        for day in context.dates:
            if not ((day < context.startdate) or (day > context.date)):
                self.tradedates.append(day)
        self.result = result()
        self.result.retSeries = pd.Series(0.0,index = self.tradedates)
        self.result.positionSeries = pd.Series(0.0,index = self.tradedates)
        print '回测引擎搭建完毕'
    def loopTime(self):
        for date in self.tradedates:
            dayret = 0
            dayPosition = 0
            daydata = context.data.ix[date]
            dayOrders = context.timedict[date]
            for No in dayOrders:
                order = context.log[No]
                dayret = dayret + order.ret
                dayPosition = dayPosition + order.cost
            self.result.retSeries[date] = dayret
            self.result.positionSeries[date] = dayPosition                
        self.result.retSeries = self.result.retSeries.cumsum().shift()
    def loop_Orders():
        pass
    def calc_alphaNbeta():
        pass
    def calc_maximumDrawndown():
        pass
    def calc_sortino():
        pass
    def calc_Var():
        pass
    def showRet(self):
        self.result.retSeries.plot()
        
        
if __name__ == '__main__':
    BacktestEngine = BacktestEngine_simpleVersion(context)
    BacktestEngine.loopTime()
    BacktestEngine.showRet()
    