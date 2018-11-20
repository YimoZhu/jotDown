# -*- coding: utf-8 -*-
"""
Created on Fri May  4 20:42:46 2018

@author: 49048
"""

'a test module'

__author__ = 'YIMO ZHU'
import sys
import tushare 

def __collect(*args,**kw):
    return tushare.get_k_data(*args,**kw)

def get_k_data(*args,**kw):
    return __collect(*args,**kw)

def sig():
    print ('working')
    
print(123)