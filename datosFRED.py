# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 15:45:59 2023

@author: julian
"""

# pip install requests

import requests 
import json
import pandas as pd
from config import FRED_API  #Debe estar en el mismo directorio del archivo principal o establecer la ruta correcta


#### Todo proceso repetitivo se puede convertir en una funcion
def respuesta_to_df(respuesta):
    statusCode = respuesta.status_code
    df = respuesta.text
    df = json.loads(df)
    df = pd.json_normalize(df)
    return df, statusCode


# ingresa a https://fred.stlouisfed.org/docs/api/api_key.html registrate y solicita tu API Key


params = {'api_key': FRED_API,
          'file_type': 'json'}


#url = "https://api.stlouisfed.org/fred/releases/dates?api_key=abcdefghijklmnopqrstuvwxyz123456"
url = "https://api.stlouisfed.org/fred/releases/dates"


response = requests.get(url,params=params)
response.status_code
### En este segmento conviertes la respuesta en un DataFrame de Pandas
calendarioFRED = response.text
calendarioFRED = json.loads(calendarioFRED)
calendarioFRED = pd.json_normalize(calendarioFRED)

calendarioFRED.columns

releases = calendarioFRED['release_dates']
releases = calendarioFRED['release_dates'][0]
tablaReleases = pd.json_normalize(calendarioFRED['release_dates'][0])


#########################################################
#########################################################
## Obtener datos de categoría por el código
urlCategoria = "https://api.stlouisfed.org/fred/category"

params = {'api_key': FRED_API,
          'file_type': 'json',
          'category_id': '10'
          }

response = requests.get(urlCategoria,params=params)

categoria, statusCategoria = respuesta_to_df(response)
categoria = pd.json_normalize(categoria['categories'][0])

#########################################################
#########################################################
## Obtener las categoría hiujo de una categoría padre

urlChilds = 'https://api.stlouisfed.org/fred/category/children'

params = {'api_key': FRED_API,
          'file_type': 'json',
          'category_id': '10'
          }

response = requests.get(urlChilds, params=params)

categoriasChild, statusChilds = respuesta_to_df(response)
categoriasChild = pd.json_normalize(categoriasChild['categories'][0])


#########################################################
#########################################################
## Obtener las Series de una Categoría

urlSeries = 'https://api.stlouisfed.org/fred/category/series'

params = {'api_key': FRED_API,
          'file_type': 'json',
          'category_id': '32250'
          }

response = requests.get(urlSeries, params=params)

seriesCategoria, statusSeries = respuesta_to_df(response)
seriesCategoria = pd.json_normalize(seriesCategoria['seriess'][0])


#########################################################
#########################################################
## Obtener los datos de la series

urlDatosSeries = 'https://api.stlouisfed.org/fred/series/observations'

params = {'api_key': FRED_API,
          'file_type': 'json',
          'series_id': 'ADPMNUSNERNSA'
          }

response = requests.get(urlDatosSeries, params=params)

datosSeries, statusDatos = respuesta_to_df(response)
datosSeries = pd.json_normalize(datosSeries['observations'][0])
datosSeries = datosSeries[['date', 'value']]

