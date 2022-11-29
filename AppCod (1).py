
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
from datetime import date, time, datetime, timedelta

#Leemos el archivo 
df1=pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv")
df1.dropna(axis = 1, thresh = int(len(df1)*.70), inplace = True)
df1.drop(["SF Find Neighborhoods","Current Police Districts","Current Supervisor Districts","Analysis Neighborhoods","Areas of Vulnerability, 2016"], axis=1,inplace=True)

df1.dropna(inplace =True)
df1['Incident Datetime'] = pd.to_datetime(df1['Incident Datetime'], format = '%Y/%m/%d %I:%M:%S %p')
df1['Incident Date'] = pd.to_datetime(df1['Incident Date'], format = '%Y/%m/%d')
h = []
for i in df1.index:
  h.append(datetime.time(datetime.strptime(df1.loc[i,'Incident Time'], '%H:%M')))
df1['Incident Time'] = h
df1['Report Datetime'] = pd.to_datetime(df1['Report Datetime'], format = '%Y/%m/%d %I:%M:%S %p')
graf1 = go.Figure()
graf1.add_trace(go.Scatter(x=df1['Incident Time'].sort_values().unique(), y=df1.groupby(['Incident Time']).mean()['Row ID'], name='Casos a través del día', line=dict(color='#00413F', width=3)))
graf1.update_layout(plot_bgcolor="white")
graf1.update_layout(xaxis_title='Hora', yaxis_title='Casos Promedio')


df1['contador'] = 1
graf2 = px.sunburst(df1, color_discrete_sequence = ['#DDFFFE','#00413F '], values='contador', path=['Police District','Analysis Neighborhood'], hover_name='Analysis Neighborhood')
graf2.update_layout(plot_bgcolor="black", title = 'Crímenes Acumulados por Distrito')


chart3 = px.area(df1, y=df1.groupby(['Incident Datetime']).count()['Row ID'], x=df1['Incident Datetime'].unique(), color_discrete_sequence = ['#00413F'])
chart3.update_layout(plot_bgcolor="white", title = 'Historial de Crimenes', xaxis_title = 'Fecha', yaxis_title='Cantidad de Crimenes')


fig5 = px.treemap(df1, color_discrete_sequence = ['#DDFFFE','#00413F'], values='contador', path=['Resolution','Incident Subcategory'], hover_name='Incident Subcategory')
fig5.update_layout(plot_bgcolor="white", title = 'Historial de Crimenes')




st.set_page_config(layout = 'wide')
st.title ("Police Department: Incident Reports")

Year = df1['Incident Year'].unique().tolist()
Descripcion = df1['Report Type Description'].unique().tolist()

Vecindario = df1['Analysis Neighborhood'].unique().tolist()


a1,a2= st.columns(2)
with a1:
    Descripcion_s = st.multiselect('Report Description: ',
                       Descripcion,
                       default = Descripcion)
with a2:
    
    Year_s = st.multiselect('Year: ',
                       Year,
                       default = Year)

Vecindario_s = st.multiselect('Neighborhood: ',
                       Vecindario,
                       default = Vecindario)


mask = (df1['Incident Year'].isin(Year_s)) & (df1['Report Type Description'].isin(Descripcion_s))& (df1['Analysis Neighborhood'].isin(Vecindario_s))


#GRAF 1

graf1 = px.scatter_mapbox(df1[mask],
                        lat="Latitude",
                        lon="Longitude",
                        hover_name="Row ID",
                        hover_data=['Analysis Neighborhood','Intersection','Police District','Report Type Description'],
                        color_discrete_sequence=["#FF2C2C"],
                        zoom=11,
                        height=500)
graf1.update_layout(mapbox_style="stamen-toner")
graf1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
graf1.update_layout(title='San Francisco Crime: HeatMap')


#GRAF2

graf2 = go.Figure()
graf2.add_trace(go.Scatter(x=df1[mask]['Incident Time'].sort_values().unique(), y=df1[mask].groupby(['Incident Time']).mean()['Row ID'], line=dict(color='#FF2C2C', width=4)))
graf2.update_layout(title='Cases per specific hour in the day', xaxis_title='Time', yaxis_title='Average of registered Cases')
graf2.update_xaxes(showgrid=False)
graf2.update_yaxes(showgrid=False)

st.plotly_chart(graf2)



#GRAF 5

graf5 = go.Figure()
graf5.add_trace(go.Scatter(x=df1[mask].sort_values(by=['Incident Datetime'])['Incident Datetime'].unique(), y=df1[mask].groupby(['Incident Datetime']).count()['Row ID'], line=dict(color='#FF2C2C', width=4)))
graf5.update_layout(title = 'Historic Crime Record: Per Year', xaxis_title = 'Date', yaxis_title='# of Crimes')
graf5.update_xaxes(showgrid=False)
graf5.update_yaxes(showgrid=False)


c1,c2 = st.columns((4,2))
with c1:
    st.plotly_chart(graf1)
with c2:
    st.plotly_chart(graf5)
    

 



