from pandas_datareader import data as pdr

import yfinance as yf

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates

import matplotlib.pyplot as plt

import pandas_datareader as pdr
import matplotlib.axis as ax
from pandas.util.testing import assert_frame_equal   

def plotPorts2(start_date,end_date):
    plt.close()
    yf.pdr_override() 




    data = pdr.get_data_yahoo("BTC-USD", start_date, end_date)
    btc = pd.DataFrame(data)

    btc = btc[['Adj Close']]
    btc.columns = ['Close']
    btc.reset_index(level=0, inplace = True)






    # In[8]:


    b = pd.DataFrame()

    for x in btc:
        b ['price'] = btc['Close']
        b['sma'] = btc['Close'].rolling(window=20).mean()
        b['std'] = btc['Close'].rolling(window=20).std()
        
        b['bolU'] = b['sma'] + (2 * b['std'] )#Calculating Upper Bound
        b['bolD'] = b['sma'] - (2 * b['std'] )#Calculating Lower Bound
        #Convert Bollinger Bands to %b - bollinger column 
        b['bollinger'] = (b['price'] - b['bolD'])/(b['bolU']-b['bolD'])

        

    bb1 = b[['price','bolU','bolD','bollinger']]
    bb1.columns = ['Price','Upper Band','Lower Band','Bollinger']
    bb1.fillna(0,inplace=True)


    # In[ ]:





    # In[9]:


    RSI = pd.DataFrame(index=btc.index)

    RSI['price'] = btc ['Close']

    RSI['val'] = None
    RSI['up'] = 0 #When there is no up  value 0 
    RSI['down'] = 0 #When there is no down   value 0 





    size = RSI.shape[0]
    dp = 14

    for x in range(size):
        if x ==0:
            continue #first day will continue
        #calculating the ups , when closing price is higher in day x than x -1  
        if RSI['price'].iloc[x] > RSI['price'].iloc[x-1]: #
            RSI['up'].iloc[x] = RSI['price'].iloc[x] - RSI['price'].iloc[x-1]
        else:
            #calculating the downs days , when closing price is lower in day x than x -1 
            RSI['down'].iloc[x] = RSI['price'].iloc[x-1]-RSI['price'].iloc[x]

        if x >= dp:
            avgUp = RSI['up'][x-dp:x].sum()/dp #calculates avg up of last dp days 
            avgDown = RSI['down'][x-dp:x].sum()/dp #calculates avg down of last dp days
            rs = avgUp/avgDown #calculation of RS
            RSI['val'].iloc[x] = 100 - 100/(1+rs)







    signals = pd.DataFrame(index=btc.index)#copy index for BTC


    signals['price'] = btc['Close']
    signals['id']= 0.0 

    signals['RSI'] = RSI['val']
    signals['RSI'].fillna(0, inplace=True)


    signals['bollinger'] = bb1['Bollinger']



    signals['id']=[np.nan for i in signals.index]

    # only  verifications for days after DPth (period of RSI) day
    signals['id'][dp:].loc[((signals['RSI'] < 30) & (signals['bollinger'] < 0))] = 1
    signals['id'][dp:].loc[((signals['RSI'] > 70) & (signals['bollinger'] > 1))] = 0
    signals['id'].ffill(inplace=True) #fill empty values with 0
    signals['id'].fillna(0,inplace=True)




    signals['buySell'] = signals['id'].diff()
    signals['buySell'].fillna(0,inplace=True)


    ###################################################################################
    # Code taken from Willems, K., 2019. (Tutorial) Python For Finance: Algorithmic Trading


    initInvestment = 100000
    stocksOwned = pd.DataFrame(index=signals.index).fillna(0.0)

    noCur = 10 #No of currency to be purchased

    stocksOwned['BTC'] = noCur*signals['id']   
      
    portfolio = pd.DataFrame(index=signals.index)
    portfolio['Holdings'] = stocksOwned['BTC'].multiply(btc['Close'], axis=0)




    buySell = stocksOwned['BTC'].diff()



    portfolio['cash'] = initInvestment - (buySell.multiply(btc['Close'], axis=0)).cumsum()


    portfolio['total'] = portfolio['cash'] + portfolio['Holdings']

    portfolio['cash'][0] = initInvestment
    portfolio['total'][0] = initInvestment

    ###################################################################################



    # In[50]:


    fig, (ax) = plt.subplots(1, 1, sharex=True)

    ax.plot(portfolio.index, portfolio['total'], label='Price')
    ax.set_xlabel('Date')
    ax.set_ylabel('Value of portfolio in USD')
    day = signals.loc[signals.buySell == 1.0].index
    day2 = signals.loc[signals.buySell == -1.0].index


    ax.scatter(x = day, y=portfolio.loc[day, 'total'], color = 'green')
    ax.scatter(x = day2, y=portfolio.loc[day2, 'total'], color = 'red')

    plt.show()

