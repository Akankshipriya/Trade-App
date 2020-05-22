import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import matplotlib.axis as ax
import yfinance as yf

def getData(startDate,endDate,cur):
    yf.pdr_override() 
    return pdr.get_data_yahoo(cur, startDate, endDate)

def emaPlot(startDate,endDate,cur,dp,dp2):
    plt.close()
    dp = int(dp)
    dp2 = int(dp2)

    data = getData(startDate,endDate,cur)
    d1 = pd.DataFrame(data)
    d1 = d1[['Adj Close']]
    
    d1.reset_index(level=0, inplace = True)
    
    d1.columns = ['Date','Close']
    
    ema1 = d1.Close.ewm(span=dp, adjust=False).mean()
    ema2 = d1.Close.ewm(span=dp2, adjust=False).mean()
    
    fig, ax = plt.subplots()
    plt.title('Exponential',fontsize=20)
    plt.xlabel('Dates',fontsize=18)
    plt.ylabel('BTS-USD',fontsize=18)
    plt.plot(d1.Date,d1.Close)
    plt.plot(d1.Date, ema1, label = cur +" "+ str(dp) +  "Day EMA", color = 'Red')
    plt.plot(d1.Date, ema2, label =  cur +" "+ str(dp2) +  "Day EMA", color = 'Green')
    plt.legend(loc='lower right')
    plt.show()