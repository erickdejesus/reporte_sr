# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 12:35:31 2016

@author: edejc
"""
# importamos librerias  para construir el mensaje
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
#importamos librerias para adjuntar
from email.mime.base import MIMEBase 
from email import encoders
from smtplib import SMTP
try:
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser

def envia_mail(Subject, texto,file):
	# Creamos una instancia de la clase y abrimos el archivo
	config = ConfigParser()
	config.read("conf.cfg")
	correo_s= config.get("DATOS", "CORREO_SALIENTE")
	passw= config.get("DATOS", "CONTRASENA")
	correo_d= config.get("DATOS", "CORREO_DESTINO")	
	# Construimos el mail
	msg = MIMEMultipart() 
	msg['To'] = correo_d
	msg['From'] = correo_s
	msg['Subject'] = Subject
	#cuerpo del mensaje en HTML y si fuera solo text puede colocar en el 2da parametro 'plain'
	msg.attach(MIMEText('<h1>Esto es una prueba</h1><p>'+texto+'El reporte se encuentra como archivo adjunto</p>','html'))
	
	#adjuntamos fichero de texto pero puede ser cualquer tipo de archivo
	#cargamos el archivo a adjuntar
	fp = open(file,'rb')
#      maintype = 'application'
#      subtype = 'octet-stream'
	adjunto = MIMEBase('multipart', 'octet-stream')
	#lo insertamos en una variable
	adjunto.set_payload(fp.read()) 
	fp.close()  
	#lo encriptamos en base64 para enviarlo
	encoders.encode_base64(adjunto) 
	#agregamos una cabecera y le damos un nombre al archivo que adjuntamos puede ser el mismo u otro
	adjunto.add_header('Content-Disposition', 'attachment', filename=file)
	#adjuntamos al mensaje
	msg.attach(adjunto) 
	
	smtp = SMTP("smtp.gmail.com", 587)
	smtp.ehlo()
	smtp.starttls()
	smtp.ehlo()
	smtp.login(correo_s, passw)
	smtp.sendmail(correo_s, correo_d, msg.as_string())
	smtp.quit()
	return()