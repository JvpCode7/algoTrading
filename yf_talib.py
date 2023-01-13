# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 10:13:47 2021

@author: julia
"""

#pip install -i https://pypi.anaconda.org/ranaroussi/simple yfinance
# pip install TA-Lib
# pip install numpy --upgrade --ignore-installed
# pip install --upgrade mplfinance
# https://github.com/TA-Lib/ta-lib-python

import yfinance as yf
import talib
from talib import RSI, BBANDS


activo = yf.Ticker("AAPL")

# get historical market data
precios = activo.history(period="24mo", interval="1d")

# Se debe trabaja con numpy arrys .to_numpy()

preciosnp = precios.to_numpy()

Open = precios['Open'].to_numpy()
high = precios['High'].to_numpy()
low = precios['Low'].to_numpy()
close = precios['Close'].to_numpy()

SimpleMA20 = talib.SMA(close, timeperiod=20)
SimpleMA40 = talib.SMA(close, timeperiod=40)
SimpleMA50 = talib.SMA(close, timeperiod=50)
SimpleMA100 = talib.SMA(close, timeperiod=100)
SimpleMA200 = talib.SMA(close, timeperiod=200)

adx = talib.ADX(high, low, close)


up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
rsi = RSI(close, timeperiod=14)

# %B Bandas de Bollinger
def bbp(price):
    up, mid, low = BBANDS(price, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    bbp = (close - low) / (up - low)
    return bbp

BollBeta = bbp(close)

# armar el nuevo DataFrame

precios['SMA20'] = SimpleMA20.tolist()
precios['SMA40'] = SimpleMA40.tolist()
precios['SMA50'] = SimpleMA50.tolist()
precios['SMA100'] = SimpleMA100.tolist()
precios['SMA200'] = SimpleMA200.tolist()
precios['ADX'] = adx.tolist()
precios['RSI'] = rsi.tolist()
precios['UP'] = up.tolist()
precios['DOWN'] = low.tolist()
precios['B'] = BollBeta.tolist()

# Crear señales delas velas japonesas
doji = talib.CDLDOJI(Open, high, low, close)

# Charts 

import matplotlib.pyplot as plt
# pip install --upgrade mplfinance
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates #Módulo avanzado para fechas de gráficos Matplotlib


precios['Date'] = precios.index

ohlc = precios.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

ohlc['Date'] = pd.to_datetime(ohlc['Date'])
ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
ohlc = ohlc.astype(float)

# Creating Subplots
fig, ax = plt.subplots()

candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

# Setting labels & titles
ax.set_xlabel('Date')
ax.set_ylabel('Price')
fig.suptitle('Daily Candlestick Chart of NIFTY50')

# Formatting Date
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()

fig.tight_layout()

plt.show()


