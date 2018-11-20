# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 12:51:33 2018

@author: 49048
"""

import numpy as np
import math
from matplotlib import pyplot as plt

x = np.linspace(-np.pi,np.pi,256,endpoint=True)
c = np.cos(x)
s = np.sin(x)

plt.figure(figsize=(10,5),dpi=80)
plt.subplot(1,1,1)

plt.plot(x,c,color='blue',linewidth=1.0,linestyle='-',label='cosine')
plt.plot(x,s,color='green',linewidth=2.0,linestyle='-',label='sin')

plt.xlim(x.min()*1.5,x.max()*1.5)
plt.ylim(c.min()*1.5,c.max()*1.5)
plt.xticks([-np.pi,0,np.pi],[r'$\frac{-\pi}{1}$','',r'$\pi$'])
plt.yticks([-1,0,1])

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0))
ax.spines['left'].set_position(('data',0))
plt.legend(loc='upper left')
#annotating a specific point
t = 2*np.pi/3
plt.plot([t,t],[0,np.cos(t)],color='blue',linestyle='--')
plt.plot([t,t],[0,np.sin(t)],color='green',linestyle='--')
plt.scatter([t,t],[np.cos(t),np.sin(t)],50,color='r')
plt.annotate('fuck you',xy=(t,np.sin(t)),fontsize=10,xytext=(10,30),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=0.5'))
plt.show()