#Importamos las librerías
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from datetime import datetime, timedelta
sns.set()

#Definimos función para guardar los datasets en dataframes.
def leerCSVdeIndices (simbolo:str):
    try:
        df = pd.read_csv(simbolo+'.csv',index_col=0)
    except:
        try:
            df = pd.read_csv('Sectores/'+simbolo+'.csv',index_col=0)
        except:
            df = pd.read_csv('Empresas/'+simbolo+'.csv',index_col=0)
    df.index = pd.to_datetime(df.index)
    return df

st.set_page_config(layout='wide')

#Ponemos la fuente
st.markdown('###### Fuente: Yahoo Finance')
ultima_actualizacion = '2023-02-23'
st.markdown('###### Ultima actualización: '+ultima_actualizacion)

#Le agregamos un título
st.title('Análisis exploratorio de datos')

st.markdown('#### Utilizando la aplicación puede realizarse un análisis gráfico de las empresas que componen el índice SP500')

#Creamos el gráfico interactivo del índice SP500 donde vamos a analizar su comportamiento a lo largo de estos 23 años
sp500 = leerCSVdeIndices('sp500')
st.write('')
st.write('')
st.write('##### Evolucion del índice SP500 desde el año 2000')
st.write('')
st.write('')
fig1 = plt.figure(figsize=(8,6))
fecha_inicio,fecha_fin = st.slider('Definir fechas de gráfico',value=(datetime.combine(sp500.index.min(), datetime.min.time()),
                                                        datetime.combine(sp500.index.max(), datetime.min.time())),
                    step=timedelta(days=1))
sns.lineplot(data=sp500[(sp500.index>fecha_inicio)&(sp500.index<fecha_fin)],y='Close',
             x=sp500[(sp500.index>fecha_inicio)&(sp500.index<fecha_fin)].index)
plt.title('SP500',fontdict={'fontsize':20})
plt.ylabel('Valor de mercado (US$)')
plt.xlabel('Fecha')
st.pyplot(fig1)

st.write('')
st.write('')

#Seleccionamos un sector para analizar a profundidad.
st.write('##### Evolucion de los distintos sectores desde el año 2000')
sp500_empresas = pd.read_csv('Empresas_SP500_con_marketcap.csv')
lista_sectores = list(sp500_empresas['GICS Sector'].unique())
lista_sectores.remove('Energy')
sector = st.selectbox('Elija sector a analizar',options=lista_sectores)

#Importamos la data de este sector.
sp_sector = leerCSVdeIndices(sector)

#Graficamos
fig2 = plt.figure(figsize=(8,6))
fecha_inicio_sec,fecha_fin_sec = st.slider('Definir fechas de gráfico',value=(datetime.combine(sp_sector.index.min(), datetime.min.time()),
                                                        datetime.combine(sp_sector.index.max(), datetime.min.time())),
                    step=timedelta(days=1))
sns.lineplot(data=sp_sector[(sp_sector.index>fecha_inicio_sec)&(sp_sector.index<fecha_fin_sec)],y='Close',
             x=sp_sector[(sp_sector.index>fecha_inicio_sec)&(sp_sector.index<fecha_fin_sec)].index)
plt.title('SP500 '+str(sector),fontdict={'fontsize':20})
plt.ylabel('Valor de mercado (US$)')
plt.xlabel('Fecha')
st.pyplot(fig2)

#Añadimos información
if st.checkbox('Mostrar información del sector',False):
    st.write('Cantidad de empresas que componen en el sector: '+ str(sp500_empresas[sp500_empresas['GICS Sector']==sector].shape[0]))
    st.dataframe(sp500_empresas[sp500_empresas['GICS Sector']==sector])

st.write('')
st.write('')

#Seleccionamos los sectores a comparar
st.write('##### Comparación de los distintos sectores desde el año 2000')
sector1,sector2 = st.multiselect('Elija sectores a comparar',options=lista_sectores,max_selections=2,default=lista_sectores[0:2])

#Importamos los datos
sp_sector1 = leerCSVdeIndices(sector1)
sp_sector2 = leerCSVdeIndices(sector2)

#Graficamos la evolucion de los 2 sectores
fig3, ax = plt.subplots(1,2,sharey=True,figsize=(12,8))
fecha_inicio_comp_sec,fecha_fin_comp_sec = st.slider('Definir fechas de gráficos',value=(datetime.combine(sp_sector1.index.min(), datetime.min.time()),
                                                        datetime.combine(sp_sector1.index.max(), datetime.min.time())),
                    step=timedelta(days=1))
sns.lineplot(data=sp_sector1[(sp_sector1.index>fecha_inicio_comp_sec)&(sp_sector1.index<fecha_fin_comp_sec)],
             y='Close',x=sp_sector1[(sp_sector1.index>fecha_inicio_comp_sec)&(sp_sector1.index<fecha_fin_comp_sec)].index,ax=ax[0])
ax[0].set_title('Indice del sector '+sector1)
sns.lineplot(data=sp_sector2[(sp_sector2.index>fecha_inicio_comp_sec)&(sp_sector2.index<fecha_fin_comp_sec)],
             y='Close',x=sp_sector2[(sp_sector2.index>fecha_inicio_comp_sec)&(sp_sector2.index<fecha_fin_comp_sec)].index,ax=ax[1])
ax[1].set_title('Indice del sector '+sector2)
st.pyplot(fig3)

#Vamos a analizar las empresas individualmente para quedarnos con unas pocas. Para ello, definimos un sector y habilitamos la elección entre las empresas de este sector.
sector_seleccionado = st.selectbox('Elija sector para profundizar',options=lista_sectores)
lista_empresas = list(sp500_empresas[sp500_empresas['GICS Sector']==sector_seleccionado]['Security'].unique())

#Antes de adentrarnos a analizar cada empresa, las comparamos en su conjunto. Ploteamos un scatterplot.
fig5 = plt.figure()
sns.scatterplot(data=sp500_empresas[sp500_empresas['GICS Sector']==sector_seleccionado],
                x='Market Capitalization',y='Current stock value')
plt.ylabel('Precio de la acción')
st.pyplot(fig5)

#Ploteamos el market cap y valor actual de la acción de la mitad con mayores valores.
fig4,ax2 = plt.subplots(1,2,figsize=(8,10))
sns.barplot(data=sp500_empresas[sp500_empresas['GICS Sector']==sector_seleccionado].sort_values(by='Market Capitalization',
            ascending=False).head(int(sp500_empresas[sp500_empresas['GICS Sector']==sector_seleccionado].shape[0]/2)),
            x='Market Capitalization',y='Symbol',orient='h',ax=ax2[0])
sns.barplot(data=sp500_empresas[sp500_empresas['GICS Sector']==sector_seleccionado].sort_values(by='Current stock value',
            ascending=False).head(int(sp500_empresas[sp500_empresas['GICS Sector']==sector_seleccionado].shape[0]/2)),
            x='Current stock value',y='Symbol',orient='h',ax=ax2[1])
st.pyplot(fig4)

#Seleccionamos las empresas dentro del sector seleccionado
empresas_seleccionadas = st.multiselect('Seleccione empresas a analizar',options=lista_empresas,max_selections=6,default=lista_empresas[0])

#Graficamos
if len(empresas_seleccionadas) == 1:
    fig6 = plt.figure(figsize=(8,6))
    simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[0]]['Symbol'].values[0]     #Buscamos el código
    empresa = leerCSVdeIndices(simbolo)                                                                     #Importamos la data
    empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()                           #Obtenemos la media móvil
    empresa_tendencia.dropna(inplace=True)                                                                  #Descartamos los nulos
    sns.lineplot(data=empresa,x=empresa.index,y='Close')                                                    #Gráficamos la evolución de los precios de la empresa
    sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values)               #Graficamos la media móvil
    plt.title(empresas_seleccionadas[0])
elif len(empresas_seleccionadas)<4:
    fig6, ax3 = plt.subplots(1,len(empresas_seleccionadas),figsize=(6+(2*len(empresas_seleccionadas)),6),sharey=True)   #Armamos la figura adaptada a la
    for i in range(len(empresas_seleccionadas)):                                                                        #cantidad de selecciones
        simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[i]]['Symbol'].values[0]
        empresa = leerCSVdeIndices(simbolo)
        empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()
        empresa_tendencia.dropna(inplace=True)
        sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[i])
        sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values)
        ax3[i].set_title(empresas_seleccionadas[i])
elif len(empresas_seleccionadas) == 4:
     fig6, ax3 = plt.subplots(2,2,figsize=(10,10),sharex=True,sharey=True)
     for i in range(len(empresas_seleccionadas)):
        simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[i]]['Symbol'].values[0]
        empresa = leerCSVdeIndices(simbolo)
        empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()
        empresa_tendencia.dropna(inplace=True)                                                 
        if i<2:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[0,i])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values)
            ax3[0,i].set_title(empresas_seleccionadas[i])
        else:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[1,i-2])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values)
            ax3[1,i-2].set_title(empresas_seleccionadas[i])
else:
    fig6, ax3 = plt.subplots(2,1+round(len(empresas_seleccionadas)/3),sharex=True,sharey=True,
                             figsize=(8+2*round(len(empresas_seleccionadas)/3),10))
    for i in range(len(empresas_seleccionadas)):
        simbolo = sp500_empresas[sp500_empresas['Security']==empresas_seleccionadas[i]]['Symbol'].values[0]
        empresa = leerCSVdeIndices(simbolo)
        empresa_tendencia = empresa['Close'].rolling(window=(100),center=True).mean()
        empresa_tendencia.dropna(inplace=True)
        if i<3:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[0,i])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values)
            ax3[0,i].set_title(empresas_seleccionadas[i])
        else:
            sns.lineplot(data=empresa,x=empresa.index,y='Close',ax=ax3[1,i-3])
            sns.lineplot(data=empresa_tendencia,x=empresa_tendencia.index,y=empresa_tendencia.values)
            ax3[1,i-3].set_title(empresas_seleccionadas[i])
st.pyplot(fig6)