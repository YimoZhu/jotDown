import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import functools
from scipy import stats
stats.chisqprob = lambda chisq, df: stats.chi2.sf(chisq, df)

data = pd.read_csv('D:\Documents\Course material\econometric\homework3\Year.csv').dropna()
stkcd = data['Stkcd']
returns = data['Yretnd']
fig = plt.figure(figsize=(14,8))
ax = returns.plot.kde(label = 'year_returns',xlim = [-1,1])
ax.legend()
keyvalue = returns.quantile(0.9)
returns = pd.DataFrame({'returns':list(returns),'isgood':0,'Stkcd':stkcd})
returns = returns.groupby('Stkcd',as_index = False).mean()
returns['isgood'] = np.where(returns['returns']>keyvalue,1,0)


data = pd.read_csv('D:\Documents\Course material\econometric\homework3\current.csv')
data = data.dropna()
data = data[['Stkcd','F010101A']]
current = data.groupby('Stkcd',as_index=0).mean()
current = current.rename(columns={'F010101A':'currentratio'})

data = pd.read_csv('D:\Documents\Course material\econometric\homework3\ROE.csv')
data = data.dropna()
data = data[['Stkcd','F050501B']]
ROE = data.groupby('Stkcd',as_index=0).mean()
ROE = ROE.rename(columns = {'F050501B':'ROE'})
'''
'''
data = pd.read_csv('D:\Documents\Course material\econometric\homework3\EPS.csv')
data = data.dropna()
data = data[['Stkcd','F090101B']]
EPS = data.groupby('Stkcd',as_index=0).mean()
EPS = EPS.rename(columns = {'F090101B':'EPS'})

data = pd.read_csv('D:\Documents\Course material\econometric\homework3\PB.csv')
data = data.dropna()
data = data[['Stkcd','F100101B']]
PB = data.groupby('Stkcd',as_index=0).mean()
PB = PB.rename(columns = {'F100101B':'PB'})

def issub(x,y):
    B = 1
    excess = []
    x = list(x)
    y = list(y)
    for i in x:
        if i not in y:
            B = 0
            excess.append(i)
    return B,excess

def getOverLap(x,y):
    pass

regress1 = functools.reduce(lambda x,y:pd.merge(x,y,on='Stkcd',left_index=True)
            ,[returns,current,ROE,EPS,PB])

def standardize(x):
    return (x-x.mean())/x.std()

for x in ['currentratio','ROE','EPS','PB']:
    regress1[x] = standardize(regress1[x])

regress1['C'] = 1
logit1 = sm.Logit(regress1['isgood'],regress1[regress1.columns[3:]])
result1 = logit1.fit()
result1.summary()

data = pd.read_csv('D:\Documents\Course material\econometric\homework3\month.csv')
data = data[['Stkcd','Trdmnt','Mretnd']]
data['isgood'] = 0

for month in set(data['Trdmnt']):
    data['isgood'] = np.where(data['Mretnd']>data[data['Trdmnt']==month].Mretnd.quantile(0.9),1,0)

foo = regress1.drop(['isgood','returns'],axis =1)
regress2 = pd.merge(data,foo,on = 'Stkcd')
del foo
osci = standardize(regress2[['Stkcd','Mretnd']].groupby('Stkcd').std().rename(columns={'Mretnd':'osci'}))

regress2 = pd.merge(regress1,osci,left_on='Stkcd',right_index=True)
    
regress2 = regress2.dropna()
logit2 = sm.Logit(regress2.isgood,regress2[regress2.columns[3:]])
result2 = logit2.fit()

