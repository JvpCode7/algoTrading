# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 15:45:59 2023

@author: julian
"""

# pip install requests
import requests 
import json
import pandas as pd
from config import FRED_API

# ingresa a https://fred.stlouisfed.org/docs/api/api_key.html registrate y solicita tu API Key

params = {'api_key': FRED_API, 'file_type': 'json'}

#url = "https://api.stlouisfed.org/fred/releases/dates?api_key=abcdefghijklmnopqrstuvwxyz123456"
url = "https://api.stlouisfed.org/fred/releases/dates"

response = requests.get(url,params=params)

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

#url = "https://api.stlouisfed.org/fred/release"
url = "https://api.stlouisfed.org/fred/release/dates"
#url = "https://api.stlouisfed.org/fred/release/tables"

params = {'api_key': FRED_API,
          'file_type': 'json',
          'release_id': '194',
          'include_release_dates_with_no_data': "true"
          }

response2 = requests.get(url,params=params)

calendarioFRED = response2.text
calendarioFRED = json.loads(calendarioFRED)
calendarioFRED = pd.json_normalize(calendarioFRED)
releases = calendarioFRED['release_dates'][0]
releases[142]

releases = calendarioFRED['releases'][0]

#### Todo proceso repetitivo se puede convertir en una funcion
def respuesta_to_df(respuesta):
    df = respuesta.text
    df = json.loads(df)
    df = pd.json_normalize(df)
    return df
