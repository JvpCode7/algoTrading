# -*- coding: utf-8 -*-
"""
@author: julian
"""

#pip install -i https://pypi.anaconda.org/ranaroussi/simple yfinance
# pip install TA-Lib
# pip install numpy --upgrade --ignore-installed
# pip install --upgrade mplfinance
# https://github.com/TA-Lib/ta-lib-python

import yfinance as yf
import talib
from talib import RSI, BBANDS
import pandas as pd

# Se carga la información de una accion desde Yahoo Finance a una Variable
activo = yf.Ticker("AAPL")

# Se trae la información de cierre diaria para un intervalo de 24 meses
precios = activo.history(period="24mo", interval="1d")

# Se debe trabaja con numpy arrys .to_numpy()
preciosnp = precios.to_numpy()

# Cada columna se convierte en una variable para clacular los indicadores técnicos
Open = precios['Open'].to_numpy()
high = precios['High'].to_numpy()
low = precios['Low'].to_numpy()
close = precios['Close'].to_numpy()

# Se calculan promedios móviles de diferentes periodos
SimpleMA20 = talib.SMA(close, timeperiod=20)
SimpleMA40 = talib.SMA(close, timeperiod=40)
SimpleMA50 = talib.SMA(close, timeperiod=50)
SimpleMA100 = talib.SMA(close, timeperiod=100)
SimpleMA200 = talib.SMA(close, timeperiod=200)

# Se calcula el ADX
adx = talib.ADX(high, low, close)

# Se calculan las bandas de bollinger
up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

# Se calcula las bandas de Bollinger
rsi = RSI(close, timeperiod=14)

# %B Bandas de Bollinger
def bbp(price):
    up, mid, low = BBANDS(price, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    bbp = (close - low) / (up - low)
    return bbp

# Se calcula el %B
BollBeta = bbp(close)

# Se agrega al dataframe de precios todos los indicadores
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

# TA-LIB también permite identificar señales de velas japonesas
doji = talib.CDLDOJI(Open, high, low, close)

# Con la información se pueden crear gráficos usando matpltlib
import matplotlib.pyplot as plt
# pip install --upgrade mplfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates #Módulo avanzado para fechas de gráficos Matplotlib

# La fecha se establece como el índice
precios['Date'] = precios.index

# Se preprara el dataset para los parámetros de velas japonesas.
ohlc = precios.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]
ohlc['Date'] = pd.to_datetime(ohlc['Date'])
ohlc['Date'] = ohlc['Date'].apply(mpl_dates.date2num)
ohlc = ohlc.astype(float)

# Crea Subplots
fig, ax = plt.subplots()
candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
# Colocando Labels y Títulos
ax.set_xlabel('Date')
ax.set_ylabel('Price')
fig.suptitle('Daily Candlestick Chart of NIFTY50')
# Darle formato a la fecha
date_format = mpl_dates.DateFormatter('%d-%m-%Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()
fig.tight_layout()
plt.show()


