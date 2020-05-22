import plotly.graph_objects as go
from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import mplfinance as mpf
import yfinance as yf
import matplotlib.pyplot as plt

def getData(startDate,endDate,cur):
    
    yf.pdr_override() 
    data = pdr.get_data_yahoo(cur, startDate, endDate)
    curv = pd.DataFrame(data)
    return curv

def plotPrice(startDate,endDate,cur):
    plt.close()
    curv = getData(startDate,endDate,cur)
    mpf.plot(curv,type='candle',style='charles',title='Candlestick Chart',ylabel=str(cur))
