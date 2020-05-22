
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
from matplotlib.dates import (YEARLY, DateFormatter,rrulewrapper, RRuleLocator, drange)



def plotTSs1(start_date,end_date,shortMa,longMa):
	yf.pdr_override() 
	plt.close()
	shortMaP = int(shortMa)
	longMaP = int(longMa)




	data = pdr.get_data_yahoo("BTC-USD", start_date, end_date)
	btc = pd.DataFrame(data)

	btc = btc[['Adj Close']]
	btc.columns = ['price']
	btc.reset_index(level=0, inplace = True)





	###################################################################################

	# Code taken from Willems, K., 2019. (Tutorial) Python For Finance: Algorithmic Trading
	#[online] DataCamp Community. Available at: <https://www.datacamp.com/community/tutorials/finance-python-trading#basics> 

	plt.close()

	signal = pd.DataFrame(index=btc.index)#copy index from BTC


	signal['id']= 0.0 




	signal['shortMA'] = btc['price'].rolling(window=shortMaP, min_periods=1).mean()#Short Moving Average Calculated

	signal['longMA'] = btc['price'].rolling(window=longMaP, min_periods=1).mean() ##Long Moving Average Calculated

	signal['id'][shortMaP:] = np.where(signal['shortMA'][shortMaP:] > signal['longMA'][shortMaP:], 1.0,0.0) #where short moving average surpasses long, id is changed to 1 

	#[shortMaP:] only for the period that is surpasses than the short moving average

	signal['buySell'] = signal['id'].diff() 

	fig = plt.figure()

	ax1 = fig.add_subplot(111,  ylabel=' Currency Price in $')

	 
	ax1.plot(btc.price) #Plot price 
	# Plot the short and long moving averages
	ax1.plot(signal['shortMA'],color = 'black', label = 'Short Moving Average')
	ax1.plot(signal['longMA'], color = 'orange', label = 'Long Moving Average' )
	ax1.legend(loc='upper right')






	# The buy signals according to buySell are plotted 
	ax1.plot(signal.loc[signal.buySell == 1.0].index, 
	         signal.shortMA[signal.buySell == 1.0],
	         '^', markersize=10, color='green')


	# The sell signals according to buySell are plotted 
	ax1.plot(signal.loc[signal.buySell == -1.0].index, 
	         signal.shortMA[signal.buySell == -1.0],
	         'v', markersize=10, color='red')


	# Show the plot
	plt.show()

###################################################################################
# Code taken from Willems, K., 2019. (Tutorial) Python For Finance: Algorithmic Trading



	portfolio = pd.DataFrame(index=signal.index)

	initInvestment = 100000
	stocksOwned = pd.DataFrame(index=signal.index).fillna(0.0)

	noCur = 10 #No of currency to be purchased

	stocksOwned['BTC'] = noCur*signal['id']   
	  

	portfolio['Holdings'] = stocksOwned['BTC'].multiply(btc['price'], axis=0)




	buySell = stocksOwned['BTC'].diff()



	portfolio['cash'] = initInvestment - (buySell.multiply(btc['price'], axis=0)).cumsum()


	portfolio['total'] = portfolio['cash'] + portfolio['Holdings']

	portfolio['cash'][0] = initInvestment
	portfolio['total'][0] = initInvestment


	
###################################################################################





	fig = plt.figure()
	ax = fig.add_subplot(111)

	ax.plot(portfolio.index, portfolio['total'], label='Price')
	ax.set_xlabel('Date')
	ax.set_ylabel('Value of Portfolio in $')


	day = portfolio.loc[signal.buySell == 1.0].index
	day2 = portfolio.loc[signal.buySell == -1.0].index

	#x co
	ax.scatter(x = day, y=portfolio.loc[day, 'total'], color = 'green', marker='^')
	ax.scatter(x = day2, y=portfolio.loc[day2, 'total'] , color = 'red',marker='^')






