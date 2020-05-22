
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
    data = pdr.get_data_yahoo(cur, startDate, endDate)
    return data
    


    


def smaPlot(startDate,endDate,cur,dp,dp2):
    plt.close()
    dp = int(dp)
    dp2 = int(dp2)

    data = getData(startDate,endDate,cur)
    d1 = pd.DataFrame(data)
    d1 = d1[['Adj Close']]
    d1.reset_index(level=0, inplace = True)
    
    d1.columns = ['Date','Close']

    movingAvgS = d1.Close.rolling(window=dp).mean()
    movingAvgL = d1.Close.rolling(window=dp2).mean()
    
    plt.title('Moving Average',fontsize=20)
    plt.xlabel('Dates',fontsize=18)
    plt.ylabel('BTS-USD',fontsize=18)
    plt.plot(d1.Date,d1.Close)
    plt.plot(d1.Date, movingAvgS, label = cur +" "+ str(dp) +  " Day SMA", color = 'Red')
    plt.plot(d1.Date, movingAvgL, label =  cur +" "+ str(dp2) +  " Day SMA", color = 'Green')
    plt.legend(loc='lower right')
    
    plt.show()