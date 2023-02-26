import requests
import pandas as pd
import yfinance as yf

pagina = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
sp500_empresas = pd.read_html(pagina.content)[0]
sp500_empresas['Symbol'].replace('BRK.B','BRK-B',inplace=True)
sp500_empresas['Symbol'].replace('BF.B','BF-B',inplace=True)

diccionario_aux = {}

for symbol in sp500_empresas.Symbol.values:
    diccionario_aux[symbol]=yf.Ticker(symbol).fast_info['marketCap']