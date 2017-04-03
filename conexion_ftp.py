# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 17:11:09 2016

@author: edejc
"""

import ftplib
import escribe_log as lg
try:
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser
# Datos FTP
#ftp_servidor = '172.17.203.61'
#ftp_usuario  = 'REPORTES_CALLC'
#ftp_clave    = 'R3portes_'
#ftp_raiz     = '/Reportes_SR' # Carpeta del servidor donde queremos subir el fichero

parametros = ConfigParser()
parametros.read("conf.cfg")
ftp_servidor= parametros.get("FTP", "SERVIDOR")
pto_ftp= parametros.get("FTP", "PUERTO")
ftp_usuario= parametros.get("FTP", "USUARIO")
ftp_clave= parametros.get("FTP", "CLAVE")
ftp_raiz = parametros.get("FTP", "RAIZ")
archivos=''
# Datos del fichero a subir
#fichero_origen = 'C:/Program Files/Anaconda3/Proyectos Erick/Reporte SR/reporte_20161214.xlsx' # Ruta al fichero que vamos a subir
#fichero_destino = 'pba.xlsx' # Nombre que tendrá el fichero en el servidor
 
def carga_Archivo(ruta_origen,fichero_origen,fichero_destino):
# Conectamos con el servidor
    try:
      s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
      try:
          f = open(ruta_origen+fichero_origen, 'rb')
          s.cwd(ftp_raiz)
          s.storbinary('STOR ' + fichero_destino, f)
          f.close()
          s.quit()
          lg.escribe_log('**Archivo correctamente subido a FTP')
      except:
#          print ("No se ha podido encontrar el fichero " + fichero_origen)
            lg.escribe_log("No se ha podido encontrar el fichero " + fichero_origen)
    except:
#        print ("No se ha podido conectar al servidor " + ftp_servidor)
        lg.escribe_log("No se ha podido conectar al servidor " + ftp_servidor)
    return ()
    
def depura_ftp():
    try:
      s = ftplib.FTP(ftp_servidor, ftp_usuario, ftp_clave)
      try:
          s.cwd(ftp_raiz)
          #listamos los archivos del directorio /pub
          archivos = s.dir()
          print (archivos)
          print ('--------')
          s.quit()
          lg.escribe_log('**Se realizó correctamente la depuración en el FTP')
      except:
#          print ("No se ha podido encontrar el fichero " + fichero_origen)
            lg.escribe_log("No se ha podido encontrar el directorio")
    except:
#        print ("No se ha podido conectar al servidor " + ftp_servidor)
        lg.escribe_log("No se ha podido conectar al servidor " + ftp_servidor)
    return()