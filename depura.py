# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 12:34:18 2017

@author: edejc
"""
import os
import filtrar_informacion as f1
from datetime import datetime, date, time, timedelta
import escribe_log as lg

def valida_directorio(ruta):
    if not os.path.exists(ruta): os.makedirs(ruta)
    return()
    
def depura_Archivos(ruta):
    formato1 = "%Y%m%d"
    nombre='reporte_'
    log= 'log'
    archivos=[]
    td = f1.dia_actual()
    rootDir = ruta
    if(td==1) or (td==15):
       lg.escribe_log('**Empieza la depuracion...')
       for dirName, subdirList, fileList in os.walk(rootDir):
#            print('Directorio encontrado: %s' % dirName)
            for fname in fileList:
                archivos.append(fname)
                
       hoy = date.today()  # Asigna fecha actual
       lg.escribe_log('**Fecha actual '+str(hoy))
       ultimo = hoy-timedelta(days=6) 
       faux= ultimo
       lg.escribe_log('**Fecha de depuracion '+str(ultimo))
       faux = faux.strftime(formato1)
        
#       print('--'+str(hoy))
#       print('++'+str(ultimo))
#       print('**'+aux)
       aux =''
       aux1 =''
       while (ultimo <= hoy):
            for ar in archivos:
                aux=nombre+str(faux)+'.xlsx'
                aux1=log+str(faux)+'.txt'
                if ar==aux:
                    archivos.remove(aux)
#                    print(ar+'*'+aux)
                elif ar==aux1:
                    archivos.remove(aux1)
#                    print(ar+'**'+aux1)
            ultimo = ultimo + timedelta(days=1) 
            faux= ultimo
            faux = faux.strftime(formato1)
#            print(faux) 
     
#    print(archivos)
       for ar in archivos:
           os.remove(ruta+ar)
                     
    return()