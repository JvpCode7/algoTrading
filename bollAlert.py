import yfinance as yf
import talib
from talib import BBANDS
import pandas as pd
import numpy as np

# Se carga la información de una accion desde Yahoo Finance a una Variable
activo = yf.Ticker("AAPL")

# Se trae la información de cierre diaria para un intervalo de 24 meses
precios = activo.history(period="max", interval="1d")
close = precios['Close'].to_numpy()

# Se calculan las bandas de bollinger
up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

# SE crea la función para la estrategia
def alertaBoll(B, amplitud, alertaPercentil):
    try:
        if B > 1 and alertaPercentil < amplitud:
            alerta = "SobreCompra"
        elif B < 0 and alertaPercentil < amplitud:
            alerta = "SobreVenta"
        elif B > 1:
            alerta = "Sobre Banda Superior sin volatilidad"
        elif B < 0:
            alerta = "Debajo Banda Inferior sin Volatilidad"
        else:
            alerta = "Sin Señal"
        return alerta
    except Exception as e:
        return str(e)

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


# Encontrar el percentil 90
alertaPercentil = np.percentile(precios['AMPLITUD'], 90)

precios['Alerta']  = precios.apply(lambda x: alertaBoll(x['B'], x['AMPLITUD'], alertaPercentil), axis=1)


# Tomar los últimos 5 años para efectos de comportamiento del activo 
#from datetime import datetime
import datetime

fechaLimite = datetime.datetime.now() - datetime.timedelta(days=5*365)
fechaLimite = np.datetime64(fechaLimite)
fechaLimite

precios.dtypes
precios['date'] = precios.index
precios.dtypes
precios['date'] = precios['date'].dt.tz_localize(None)
precios.dtypes


precios = precios[precios['date'] > fechaLimite]

precios['AMPLITUD'].plot()
precios['AMPLITUD'].hist(bins=100)


# Encontrar el percentil 90
alertaPercentil = np.percentile(precios['AMPLITUD'], 90)



# Traer últimos 30 datos para caluclar parámetros de banda
# Si el porcentaje B es negativo o superior a 1 y la amplitud es mayor al 95% se da alerta

preciosHoy = activo.history(period="30d", interval="1d")
close = preciosHoy['Close'].to_numpy()

# Se calculan las bandas de bollinger
up, mid, low = BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

BollBeta = bbp(close)


preciosHoy['UP'] = up.tolist()
preciosHoy['MID'] = mid.tolist()
preciosHoy['DOWN'] = low.tolist()
preciosHoy['B'] = BollBeta.tolist()

preciosHoy['AMPLITUD'] = preciosHoy['UP'] / preciosHoy['DOWN'] - 1

preciosHoy['Alerta']  = preciosHoy.apply(lambda x: alertaBoll(x['B'], x['AMPLITUD'], alertaPercentil), axis=1)
