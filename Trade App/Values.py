import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates

import matplotlib.pyplot as plt
import pandas_datareader as pdr
import matplotlib.axis as ax
from pandas.util.testing import assert_frame_equal

from pandas_datareader import data as pdr

import yfinance as yf


def getData(startDate,endDate,cur):
    
    yf.pdr_override() 
    histData = pdr.get_data_yahoo(cur, startDate, endDate)
    return histData
    

def getSMA(startDate,endDate,cur,dp):
    
    dp = int(dp)
    data = getData(startDate,endDate,cur)
    d1 = pd.DataFrame(data)
    d1 = d1[['Adj Close']]
    d1.reset_index(level=0, inplace = True)
    d1.columns = ['Date','Close']
    movingAvgS = d1.Close.rolling(window=dp).mean()
    movingAvgS.fillna(0,inplace=True)
    ret = pd.concat([d1.Date,d1.Close,movingAvgS],axis=1)
    ret.columns = ['Date','Currency Price','SMA']
    
    return ret

    

def getEMA(startDate,endDate,cur,dp):
    dp = int(dp)
    data = getData(startDate,endDate,cur)
    d1 = pd.DataFrame(data)
    d1 = d1[['Adj Close']]
    
    d1.reset_index(level=0, inplace = True)
    
    d1.columns = ['Date','Close']
    
    ema1 = d1.Close.ewm(span=dp, min_periods=dp).mean() #exponential weighted mean
    ema1.fillna(0,inplace=True)
    ret = pd.concat([d1.Date,d1.Close,ema1],axis=1)
    ret.columns = ['Date','Currency Price','EMA']
    
    return ret 


    



def getRSI(startDate,endDate,cur,dp):
    data = getData(startDate,endDate,cur)
    RSI = pd.DataFrame(index=data.index)
    dp=int(dp)
    RSI['price'] = data [['Adj Close']]
    
    RSI['val'] = None
    RSI['up'] = 0 #When there is no up  value 0 
    RSI['down'] = 0 #When there is no down   value 0 
    
    size = RSI.shape[0]

    for x in range(size):
        if x ==0:
            continue #first day will continue
        #calculating the up days , when closing price is higher in day x than x -1  
        if RSI['price'].iloc[x] > RSI['price'].iloc[x-1]: #
            RSI['up'].iloc[x] = RSI['price'].iloc[x] - RSI['price'].iloc[x-1]
        else:
            #calculating the downs days , when closing price is lower in day x than x -1 
            RSI['down'].iloc[x] = RSI['price'].iloc[x-1]-RSI['price'].iloc[x]
            
        if x >= dp:
            avgUp = RSI['up'][x-dp:x].sum()/dp #calculates avg up of last dp days 
            avgDown = RSI['down'][x-dp:x].sum()/dp #calculates avg down of last dp days
            rs = avgUp/avgDown #calculation of RS
            RSI['val'].iloc[x] = 100 - 100/(1+rs) #calculation of RSI
            
    RSI=RSI.reset_index()
    RSI = pd.concat([RSI.Date,RSI.price,RSI.val],axis=1) #concat columns 
    RSI.columns = ['Date','Currency Price','RSI']   
    #RSI.fillna(0,inplace=True) 

    return RSI            
   


def plotRSI(startDate,endDate,cur,dp):
    plt.close()
    RSI = getRSI(startDate,endDate,cur,dp)
    xc2 = []
    for x in range(len(RSI)):
        xc2.append(70)

    xc1 = []
    for y in range(len(RSI)):
        xc1.append(30)
    fig, ax = plt.subplots()
    rsiLine = ax.plot(RSI.Date,RSI.RSI , label = str(dp) + ' Day RSI')
    upperLine = ax.plot(RSI.Date,xc2, '--', color = 'red')
    LowerLine = ax.plot(RSI.Date,xc1, '--', color = 'green')
    s1= datetime.strptime(startDate, '%Y-%m-%d')
    plt.title('Resistance Strength Index',fontsize=20)
    plt.xlabel('Dates',fontsize=18)
    plt.ylabel('RSI',fontsize=18)
    plt.text(s1, 75, 'Overbought')
    plt.text(s1, 35, 'Oversold')
    plt.legend(loc='upper right')
    plt.show()
