# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 12:48:57 2017

@author: edejc
"""
import filtrar_informacion as f1
try:
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser
    
parametros = ConfigParser()
parametros.read("conf.cfg")
carpeta = parametros.get("CARPETA", "RUTA")
    
def escribe_log(texto):
    var_fecha=f1.fecha_actual()
    ruta_log = carpeta+'log'+str(var_fecha)+'.txt'
#    print(var_fecha)
    archi=open(ruta_log,'a')
    archi.write(texto)
    archi.write('\n')
    return()
    