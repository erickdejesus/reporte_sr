# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:16:31 2016

@author: edejc
"""

import time
import pandas as pd
from datetime import datetime, date,timedelta

suma_v=0

def f(row):
    var='SR'
    return (var)
    
def s(row):
    var1 = 0
    return var1
    
def set_suma_v(valor):
    suma_v=valor
    return ()

def t(row):
    return (suma_v)

def dia_reporte():
    formato1 = "%Y%m%d"
    hoy = date.today()  # Asigna fecha actual
    itoday = hoy-timedelta(days=1) 
    itoday = itoday.strftime(formato1)
#    print(itoday)
    return(itoday)
    
def dia_actual():
    hoy = time.strftime("%d")
    hoy = int(hoy)
    return hoy
    
def fecha_actual():
    itoday = time.strftime("%d")
    fecha= time.strftime("%Y%m")
    fecha=str(fecha)+str(itoday)
    return(fecha)
    
def prueba():
    return ('20161206')
    
def filtro(consulta,db,area,fecha,grupo,col1,col2,col3):
    consulta=consulta.replace('parametro',area)
    consulta=consulta.replace('fechas',fecha)
    consulta=consulta.replace('grupos',grupo)
    data = pd.read_sql(consulta,db,index_col=None)
#    print(data)
#    data=data.loc[data[col1].isnull(), col1] = 'Blank'
    data=data.pivot(index=col1, columns=col2, values=col3)
    return (data)
    
def pivote(data,col1,col2,col3):
    data=data.pivot(index=col1, columns=col2, values=col3)
    return(data)

def reordena(data,valor1,valor2,col1,col2,col3):
    indexv=data.index
    valores=data.values
    diccd = {valor1 : pd.Series(indexv), valor2 : pd.Series(valores)}
    df = pd.DataFrame(diccd)
    df["SR"] = df.apply(f, axis=1)
    df=df.pivot(index=col1, columns=col2, values=col3)
    return (df)
    
def grand_total(data1):
    data1['Grand_total'] = data1.apply(s, axis=1)
    return(data1)
    
def total(df):
    df["SR"] = df.apply(t, axis=1)
    return(df)