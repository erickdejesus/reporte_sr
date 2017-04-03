# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 13:11:12 2016

@author: edejc
"""

import cx_Oracle
import escribe_log as lg
try:
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser
db = None
#usuario = 'USR_SOPORTE'
#passw = 'USR_SOPORTE'
#URL1 = 'crmpdb-scan.puerto.liverpool.com.mx:1527/CRMP' #CRM_PRODUCCION
parametros = ConfigParser()
parametros.read("conf.cfg")
URL1 = parametros.get("DB", "URL")
usuario = parametros.get("DB", "USER")
passw = parametros.get("DB", "PASS")


def open_conn():    
    try:
        db=cx_Oracle.connect(usuario,passw,URL1)
        lg.escribe_log('** Conexion Base de Datos establecida')
    except cx_Oracle.DatabaseError as rep:
        msg='Error:',str(db)+str(rep)
#        print(msg)
        lg.escribe_log('-- Error conexion'+msg)
        
    return db
    
def close_conn():
    try:
        db.close()
        lg.escribe_log('** Conexion Base de Datos cerrada')
    except cx_Oracle.DatabaseError as rep:
        msg='Error:',str(db)+str(rep)
#        print(msg)
        lg.escribe_log('** Error conexion'+msg)
    return ()
    