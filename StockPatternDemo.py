# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:35:45 2017

@author: Roy
"""
 
import talib as ta
import tushare as ts
import numpy as np
import pandas as pd
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
from pyqtgraph.Point import Point


class CandlestickItem(pg.GraphicsObject):
    '''K线图类'''
    def __init__(self):
        pg.GraphicsObject.__init__(self)
        self.flagHasData = False

    def set_data(self, data):
        self.data = data  # data must have fields: time, open, close, min, max
        self.flagHasData = True
        self.generatePicture()
        self.informViewBoundsChanged()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w'))
        w = (self.data[1][0] - self.data[0][0]) / 3.
        for (t, open, close, min, max) in self.data:
            if open > close:
                p.setBrush(pg.mkBrush('g'))
                p.setPen(pg.mkPen('g'))
                p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))                
            else:
                p.setBrush(pg.mkBrush('r'))
                p.setPen(pg.mkPen('r'))
                p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))                        
            p.drawRect(QtCore.QRectF(t-w, open, w*2, close-open))
        p.end()

    def paint(self, p, *args):
        if self.flagHasData:
            p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())

    
class StockPatternDemo(object):
    '''check stock pattern'''
    def __init__(self,stockList=[],T='D'):
        '''init'''
        self.stockList = stockList #Target Stock List
        self.T  = T #The period of K
        self.dataList = []#dataframe list include the K data
        if self.T not in ['M','W','D','60','30','15','5']:
            print 'Wrong T!'
            self.T = 'D'
        self.resultList = []#output list tmp
        self.timeIndex = [] #time index
    def getData(self):
        '''From tushare get the data'''
        for stock in self.stockList:
            df = ts.get_k_data(stock, ktype=self.T)[-300:] #reduce the test time
            df.index = range(0,len(df))
            self.timeIndex = df.date
            self.dataList.append(df)
        print 'Data Loaded'
        
    def peel_remain(self,sigList):
        '''peel the sigal list which contains both + & -'''
        list_positive = np.where(sigList<0,0,sigList)
        list_negative = np.where(sigList>0,0,sigList)
        return (list_positive,list_negative)
        
    def checkResult(self,result,name,type):
        ''''belong to checkPattern()'''
        if max(result) == min(result) == 0: #the target pattern did not exist
            return
        if (type == 'check') and (min(result) < 0) and (max(result) > 0): #need peeling
            print 'peeling'
            list1,list2 = self.peel_remain(result)
            tmp1 = [list1,name,'up',list(self.timeIndex[list(result.nonzero()[0])])]
            tmp2 = [list2,name,'down',list(self.timeIndex[list(result.nonzero()[0])])]
            self.resultList.append(tmp1)
            self.resultList.append(tmp2)
            return
        elif (type == 'check') and (max(result) > 0):
            type = 'up'
        elif (type == 'check') and (min(result) < 0):
            type = 'down'    
        tmp = [result,name,type,list(self.timeIndex[list(result.nonzero()[0])])]
        self.resultList.append(tmp)
    def process2df(self):
        '''将resultList处理为df'''
        name_list = []
        type_list = []
        time_list = []
        sig_list = []
        for item in self.resultList:
            name_list.append(item[1])
            type_list.append(item[2])
            time_list.append(item[3])
            sig_list.append(item[0])
        dict1 = {'name':name_list,'type':type_list,'time':time_list,'sig':sig_list}
        self.result_df = pd.DataFrame(dict1)
        self.result_df.set_index(self.result_df.time,inplace=True)
        self.result_df.sort_index(inplace=True)        




    def checkPattern(self, df):
        #downside signal
        tmp_type = 'down'
        result = ta.CDL2CROWS(df.open.values, df.high.values, df.low.values, df.close.values) #Two Crows 两只乌鸦
        self.checkResult(result,u'TwoCrows两只乌鸦',tmp_type)
        result = ta.CDL3BLACKCROWS(df.open.values, df.high.values, df.low.values, df.close.values)#Three Black Crows 三只黑乌鸦
        self.checkResult(result,u'ThreeBlackCrows三只黑乌鸦',tmp_type)
        result = ta.CDL3LINESTRIKE(df.open.values, df.high.values, df.low.values, df.close.values)#Three-Line Strike 三线震荡
        self.checkResult(result,u'Three-LineStrike三线震荡',tmp_type)
        result = ta.CDLADVANCEBLOCK(df.open.values, df.high.values, df.low.values, df.close.values)#Advance Block 推进
        self.checkResult(result,u'AdvanceBlock推进',tmp_type)
        result = ta.CDLBREAKAWAY(df.open.values, df.high.values, df.low.values, df.close.values)#Breakaway 分离        
        self.checkResult(result,u'Breakaway分离',tmp_type)
        result = ta.CDLDARKCLOUDCOVER(df.open.values, df.high.values, df.low.values, df.close.values, penetration=0)#Dark Cloud Cover 乌云盖       
        self.checkResult(result,u'DarkCloudCover乌云盖',tmp_type)
        result = ta.CDLEVENINGDOJISTAR(df.open.values, df.high.values, df.low.values, df.close.values, penetration=0)#Evening Doji Star 黄昏十字星
        self.checkResult(result,u'EveningDojiStar黄昏十字星',tmp_type)
        result = ta.CDLEVENINGSTAR(df.open.values, df.high.values, df.low.values, df.close.values, penetration=0)#Evening Star 黄昏之星
        self.checkResult(result,u'EveningStar黄昏之星',tmp_type)
        result = ta.CDLHANGINGMAN(df.open.values, df.high.values, df.low.values, df.close.values)#Hanging Man 吊人
        self.checkResult(result,u'HangingMan吊人',tmp_type)
        result = ta.CDLIDENTICAL3CROWS(df.open.values, df.high.values, df.low.values, df.close.values)#Identical Three Crows 相同的三只乌鸦
        self.checkResult(result,u'IdenticalThreeCrows相同的三只乌鸦',tmp_type)
        result = ta.CDLINNECK(df.open.values, df.high.values, df.low.values, df.close.values) #In-Neck Pattern 颈纹
        self.checkResult(result,u'In-NeckPattern颈纹',tmp_type)
        result = ta.CDLONNECK(df.open.values, df.high.values, df.low.values, df.close.values)#On-Neck Pattern 颈型
        self.checkResult(result,u'On-NeckPattern颈型',tmp_type)
        result = ta.CDLSHOOTINGSTAR(df.open.values, df.high.values, df.low.values, df.close.values)#ShCoting Star 流星
        self.checkResult(result,u'ShCotingStar流星',tmp_type)
        result = ta.CDLSTALLEDPATTERN(df.open.values, df.high.values, df.low.values, df.close.values)#Stalled Pattern 停滞模式
        self.checkResult(result,u'StalledPattern停滞模式',tmp_type)
        result = ta.CDLTHRUSTING(df.open.values, df.high.values, df.low.values, df.close.values)#Thrusting Pattern 推模式
        self.checkResult(result,u'ThrustingPattern推模式',tmp_type)
        result = ta.CDLUPSIDEGAP2CROWS(df.open.values, df.high.values, df.low.values, df.close.values)#Upside Gap Two Crows 双飞乌鸦
        self.checkResult(result,u'UpsideGapTwoCrows双飞乌鸦',tmp_type)
        
        #upside signal
        tmp_type = 'up'
        result = ta.CDL3STARSINSOUTH(df.open.values, df.high.values, df.low.values, df.close.values)#Three Stars In The South 南方三星
        self.checkResult(result,u'ThreeStarsInTheSouth南方三星',tmp_type)        
        result = ta.CDL3WHITESOLDIERS(df.open.values, df.high.values, df.low.values, df.close.values)#Three Advancing White Soldiers 三白兵
        self.checkResult(result,u'ThreeAdvancingWhiteSoldiers三白兵',tmp_type)
        result = ta.CDLCONCEALBABYSWALL(df.open.values, df.high.values, df.low.values, df.close.values)#Concealing Baby Swallow 藏婴吞没形态
        self.checkResult(result,u'ConcealingBabySwallow藏婴吞没形态',tmp_type)
        result = ta.CDLHAMMER(df.open.values, df.high.values, df.low.values, df.close.values)#Hammer 锤
        self.checkResult(result,u'Hammer锤',tmp_type)
        result = ta.CDLHOMINGPIGEON(df.open.values, df.high.values, df.low.values, df.close.values)#Homing Pigeon 信鸽    
        self.checkResult(result,u'HomingPigeon信鸽',tmp_type)
        result = ta.CDLINVERTEDHAMMER(df.open.values, df.high.values, df.low.values, df.close.values) #Inverted Hammer 倒锤
        self.checkResult(result,u'InvertedHammer倒锤',tmp_type)
        result = ta.CDLLADDERBOTTOM(df.open.values, df.high.values, df.low.values, df.close.values)#Ladder Bottom 梯底
        self.checkResult(result,u'LadderBottom梯底',tmp_type)
        result = ta.CDLMATCHINGLOW(df.open.values, df.high.values, df.low.values, df.close.values)#Matching Low 匹配低
        self.checkResult(result,u'MatchingLow匹配低',tmp_type)
        result = ta.CDLMORNINGDOJISTAR(df.open.values, df.high.values, df.low.values, df.close.values, penetration=0)#Morning Doji Star 早晨十字星
        self.checkResult(result,u'MorningDojiStar早晨十字星',tmp_type)
        result = ta.CDLMORNINGSTAR(df.open.values, df.high.values, df.low.values, df.close.values, penetration=0)#Morning Star 晨星
        self.checkResult(result,u'MorningStar晨星',tmp_type)
        result = ta.CDLPIERCING(df.open.values, df.high.values, df.low.values, df.close.values)#Piercing Pattern 穿孔模式
        self.checkResult(result,u'PiercingPattern穿孔模式',tmp_type)
        result = ta.CDLTAKURI(df.open.values, df.high.values, df.low.values, df.close.values)#Takuri (Dragonfly Doji with very long lower shadow) 托里
        self.checkResult(result,u'Takuri(DragonflyDojiwithverylonglowershadow)托里',tmp_type)
        result = ta.CDLTASUKIGAP(df.open.values, df.high.values, df.low.values, df.close.values)#Tasuki Gap 翼隙
        self.checkResult(result,u'TasukiGap翼隙',tmp_type)
        result = ta.CDLUNIQUE3RIVER(df.open.values, df.high.values, df.low.values, df.close.values)#Unique 3 River 独特的三河
        self.checkResult(result,u'Unique3River独特的三河',tmp_type)
        
        #neutral signal  
        tmp_type = 'neutral'
        result = ta.CDLCLOSINGMARUBOZU(df.open.values, df.high.values, df.low.values, df.close.values)#Closing Marubozu 收盘光头光脚
        self.checkResult(result,u'ClosingMarubozu收盘光头光脚',tmp_type)        
        result = ta.CDLDOJI(df.open.values, df.high.values, df.low.values, df.close.values)#Doji 十字星
        self.checkResult(result,u'Doji十字星',tmp_type)
        result = ta.CDLDRAGONFLYDOJI(df.open.values, df.high.values, df.low.values, df.close.values)#Dragonfly Doji 蜻蜓十字星      
        self.checkResult(result,u'DragonflyDoji蜻蜓十字星',tmp_type)
        result = ta.CDLGRAVESTONEDOJI(df.open.values, df.high.values, df.low.values, df.close.values)#Gravestone Doji 墓碑十字线
        self.checkResult(result,u'GravestoneDoji墓碑十字线',tmp_type)        
        result = ta.CDLHIGHWAVE(df.open.values, df.high.values, df.low.values, df.close.values)#High-Wave Candle 长脚十字线
        self.checkResult(result,u'High-WaveCandle长脚十字线',tmp_type)
        result = ta.CDLLONGLEGGEDDOJI(df.open.values, df.high.values, df.low.values, df.close.values)#Long Legged Doji 长腿十字线
        self.checkResult(result,u'LongLeggedDoji长腿十字线',tmp_type)
        result = ta.CDLLONGLINE(df.open.values, df.high.values, df.low.values, df.close.values) #Long Line Candle 长线
        self.checkResult(result,u'LongLineCandle长线',tmp_type)
        result = ta.CDLMARUBOZU(df.open.values, df.high.values, df.low.values, df.close.values)#Marubozu 光头光脚
        self.checkResult(result,u'Marubozu光头光脚',tmp_type)
        result = ta.CDLRICKSHAWMAN(df.open.values, df.high.values, df.low.values, df.close.values)#Rickshaw Man 车夫
        self.checkResult(result,u'RickshawMan车夫',tmp_type)
        result = ta.CDLSHORTLINE(df.open.values, df.high.values, df.low.values, df.close.values)#Short Line Candle 短线
        self.checkResult(result,u'ShortLineCandle短线',tmp_type)
        result = ta.CDLSPINNINGTOP(df.open.values, df.high.values, df.low.values, df.close.values)#Spinning Top 陀螺
        self.checkResult(result,u'SpinningTop陀螺',tmp_type)

        #Not sure signal
        result = ta.CDL3INSIDE(df.open.values, df.high.values, df.low.values, df.close.values)#Three Inside Up/Down 三内上下震荡
        self.checkResult(result,u'ThreeInsideUp/Down三内上下震荡','check')
        result = ta.CDL3OUTSIDE(df.open.values, df.high.values, df.low.values, df.close.values)#Three Outside Up/Down 三外下震荡
        self.checkResult(result,u'ThreeOutsideUp/Down三内上下震荡','check')
        result = ta.CDLABANDONEDBABY(df.open.values, df.high.values, df.low.values, df.close.values, penetration=0)#Abandoned Baby 弃婴
        self.checkResult(result,u'AbandonedBaby弃婴','check')
        result = ta.CDLBELTHOLD(df.open.values, df.high.values, df.low.values, df.close.values)#Belt-hold 带住
        self.checkResult(result,u'Belt-hold带住','check')
        result = ta.CDLCOUNTERATTACK(df.open.values, df.high.values, df.low.values, df.close.values)#Counterattack
        self.checkResult(result,u'Counterattack','check')
        result = ta.CDLDOJISTAR(df.open.values, df.high.values, df.low.values, df.close.values)#Doji Star 十字星
        self.checkResult(result,u'DojiStar十字星','check')
        result = ta.CDLENGULFING(df.open.values, df.high.values, df.low.values, df.close.values)#Engulfing Pattern 吞没
        self.checkResult(result,u'EngulfingPattern吞没','check')
        result = ta.CDLGAPSIDESIDEWHITE(df.open.values, df.high.values, df.low.values, df.close.values)#Up/Down-gap side-by-side white lines 上/下间隙并排的白色线条
        self.checkResult(result,u'Up/Down-gap_side-by-side_whitelines上/下间隙并排的白色线条','check')
        result = ta.CDLHARAMI(df.open.values, df.high.values, df.low.values, df.close.values)#Harami Pattern 阴阳线(反吞没)
        self.checkResult(result,u'HaramiPattern阴阳线(反吞没)','check')
        result = ta.CDLHARAMICROSS(df.open.values, df.high.values, df.low.values, df.close.values)#Harami Cross Pattern 交叉阴阳线
        self.checkResult(result,u'Harami Cross Pattern 交叉阴阳线','check')
        result = ta.CDLHIKKAKE(df.open.values, df.high.values, df.low.values, df.close.values)#Hikkake Pattern 陷阱
        self.checkResult(result,u'HikkakePattern陷阱','check')
        result = ta.CDLHOMINGPIGEON(df.open.values, df.high.values, df.low.values, df.close.values)#Modified Hikkake Pattern 改良的陷阱
        self.checkResult(result,u'ModifiedHikkakePattern改良的陷阱','check')
        result = ta.CDLKICKING(df.open.values, df.high.values, df.low.values, df.close.values)#Kicking 踢
        self.checkResult(result,u'Kicking踢','check')
        result = ta.CDLKICKINGBYLENGTH(df.open.values, df.high.values, df.low.values, df.close.values)#Kicking-bull/bear determined by the longer marubozu 踢牛/踢熊
        self.checkResult(result,u'Kicking-bull/bear_determined_by_the_longer_marubozu踢牛/踢熊','check')
        result = ta.CDLMATHOLD(df.open.values, df.high.values, df.low.values, df.close.values,penetration=0)#Mat Hold 垫住
        self.checkResult(result,u'MatHold垫住','check')
        result = ta.CDLRISEFALL3METHODS(df.open.values, df.high.values, df.low.values, df.close.values)#Rising/Falling Three Methods 上升/下降三法
        self.checkResult(result,u'Rising/FallingThree Methods上升/下降三法','check')
        result = ta.CDLSEPARATINGLINES(df.open.values, df.high.values, df.low.values, df.close.values)#Separating Lines 分割线
        self.checkResult(result,u'SeparatingLines分割线','check')
        result = ta.CDLSTICKSANDWICH(df.open.values, df.high.values, df.low.values, df.close.values)#Stick Sandwich 棍子三明治
        self.checkResult(result,u'StickSandwich棍子三明治','check')
        result = ta.CDLTRISTAR(df.open.values, df.high.values, df.low.values, df.close.values)#Tristar Pattern 三星模式
        self.checkResult(result,u'TristarPattern三星模式','check')
        result = ta.CDLXSIDEGAP3METHODS(df.open.values, df.high.values, df.low.values, df.close.values)#Upside/Downside Gap Three Methods 上行/下行缺口三方法
        self.checkResult(result,u'Upside/DownsideGapThreeMethods上行/下行缺口三方法','check')
        
        print 'Checked!'
        return self.resultList
        
    def run_patternCheck(self):
        self.getData()
        self.checkPattern(self.dataList[0])
        self.process2df()        
        return self.result_df        
        
    
    
#crosshair demo    
a = StockPatternDemo(['000006'],'D')
result = a.run_patternCheck()

df = a.dataList[0]
df1 = df[['date','open','close','low','high']] 
df1.date = np.arange(0,len(df1))#set time
data = np.asarray(df1)  

#generate layout
app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.setWindowTitle('Pattern')
label = pg.LabelItem(justify='right')
win.addItem(label)
p1 = win.addPlot(row=1, col=0) #Last Price
p1.plot(df['close'], pen="w")       #收盘价图
p2 = win.addPlot(row=2, col=0) #K


region = pg.LinearRegionItem()
region.setZValue(10)
p2.addItem(region, ignoreBounds=True)
p1.setAutoVisible(y=True)
xAxis = np.arange(0, len(df))
item = CandlestickItem()    #K图
item.set_data(data)
p2.addItem(item)
def update():
    region.setZValue(10)
    minX, maxX = region.getRegion()
    p1.setXRange(minX, maxX, padding=0)    
region.sigRegionChanged.connect(update)

def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)

p1.sigRangeChanged.connect(updateRegion)

region.setRegion([50, 100])

#cross hair
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
vLine2 = pg.InfiniteLine(angle=90, movable=False)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)
p2.addItem(vLine2, ignoreBounds=True)

vb = p1.vb

def mouseMoved(evt):
    pos = evt[0]  # using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if index > 0 and index < len(df.close):
            label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), df.close[index], df.close[index]))
        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())
        vLine2.setPos(mousePoint.x())


proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
#p1.scene().sigMouseMoved.connect(mouseMoved)


if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()