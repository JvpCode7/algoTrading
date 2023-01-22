#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 19:01:07 2023

@author: julian
"""

import yfinance as yf
import talib
from talib import BBANDS
import pandas as pd

# Se carga la información de una accion desde Yahoo Finance a una Variable
activo = yf.Ticker("AAPL")

# Se trae la información de cierre diaria para un intervalo de 24 meses
precios = activo.history(period="max", interval="1d")
close = precios['Close'].to_numpy()

# Se calculan las bandas de bollinger
up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)



# %B Bandas de Bollinger
def bbp(price):
    up, mid, low = BBANDS(price, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    bbp = (close - low) / (up - low)
    return bbp

# Se calcula el %B
BollBeta = bbp(close)


precios['UP'] = up.tolist()
precios['MID'] = mid.tolist()
precios['DOWN'] = low.tolist()
precios['B'] = BollBeta.tolist()

# Se estandariza la diferencia histórica entre la banda superior e inferior
# UP /  DOWN - 1
precios['AMPLITUD'] = precios['UP'] / precios['DOWN'] - 1

precios['AMPLITUD'].plot()
precios['AMPLITUD'].hist(bins=100)

precios = precios[precios['AMPLITUD'] < 1]

precios['AMPLITUD'].plot()
precios['AMPLITUD'].hist(bins=100)
