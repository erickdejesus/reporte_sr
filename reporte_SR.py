# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 12:03:15 2016

@author: edejc
"""
import pandas as pd
import conexion as con
import createFile as cfile
import filtrar_informacion as f1
#import envio_correo as mimail
import conexion_ftp as cftp
import escribe_log as lg
import depura as depura
try:
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser

Consulta = ""
resultado = None
var_fecha=""
db = None
# Creamos una instancia de la clase y abrimos el archivo
config = ConfigParser()
config.read("consultas.cfg")
parametros = ConfigParser()
parametros.read("conf.cfg")
reporte2 = ConfigParser()
reporte2.read("consultas2.cfg")
fecha_acum= config.get("CONSULTAS", "FECHA_ACUM")
fecha_ante= config.get("CONSULTAS", "FECHA_ANTE")
consulta= config.get("CONSULTAS", "CONSULTA")
conteo = config.get("CONSULTAS", "CONTEO")
area = config.get("CONSULTAS", "P_AREA")
fcr = config.get("CONSULTAS", "P_FCR")
grupos_a= config.get("CONSULTAS", "GRUPO_A")
grupos_f= config.get("CONSULTAS", "GRUPO_F")
var_fecha=f1.dia_reporte()
fecha_acum=fecha_acum.replace('FECHA_VAR',var_fecha)
fecha_ante=fecha_ante.replace('FECHA_VAR',var_fecha)
c_folios = reporte2.get("CONSULTAS", "FOLIOS")
c_porcentaje = reporte2.get("CONSULTAS", "PORCENTAJE")
c_backlog = reporte2.get("CONSULTAS", "BACKLOG")
c_promedio = reporte2.get("CONSULTAS", "PROMEDIO")
c_pro1 = reporte2.get("CONSULTAS", "PROM1")
c_pro2 = reporte2.get("CONSULTAS", "PROM2")
carpeta = parametros.get("CARPETA", "RUTA")
depura.valida_directorio(carpeta)
#c=db.cursor()
#print(var_fecha)
texto = '**************** Inicia el proceso del reporte '+str(var_fecha)+'************'
lg.escribe_log(texto)
db=con.open_conn()
try:
#    print(db)   
#    db=con.open_conn(user_db,pass_db,url_db)
#    print(Consulta)
    sqlt = consulta + " " + fecha_acum
#    print('Creacion consulta')
    lg.escribe_log('**Creacion consulta datos completos')
    resultado = pd.read_sql(sqlt,db,index_col=None)
    resultado.loc[resultado['AREA'].isnull(), 'AREA'] = 'Blank'
    resultado.loc[resultado['FCR'].isnull(), 'FCR'] = 'Blank'
#    print('Datos acumulados completos...')
    lg.escribe_log('Datos acumulados completos...')
    aux_sql= conteo
    fecha_acum = ' '+fecha_acum+' '
    f_areas=f1.filtro(aux_sql,db,area,fecha_acum,grupos_a,'AREA','ESTADO','VALORES')
#    f_areas = resultado.sort_values(['AREA'], ascending=False).groupby(['AREA', 'ESTADO']).agg({'ESTADO': np.size})
    aux_sql= conteo
    f_FCR= f1.filtro(aux_sql,db,fcr,fecha_acum,grupos_f,'FCR','ESTADO','VALORES')
#    f_FCR = resultado.sort_values(['FCR'], ascending=True).groupby(['FCR', 'ESTADO']).agg({'ESTADO': np.size})
    f_est = resultado.groupby('ESTADO').size()
    f_est= f1.reordena(f_est,'Estado','Valor','SR','Estado','Valor')
#    f_est= pd.DataFrame(f_est)
#    res_estatus = f1.conteo_DataF(f_est,'ESTATUS')
#    print('Cifras de acumulados completos...')
    lg.escribe_log('Cifras de acumulados completos...')
    aux_sql= conteo
    fecha_ante = ' '+fecha_ante+' '
    f_areas_ante=f1.filtro(aux_sql,db,area,fecha_ante,grupos_a,'AREA','ESTADO','VALORES')
#    f_areas = resultado.sort_values(['AREA'], ascending=False).groupby(['AREA', 'ESTADO']).agg({'ESTADO': np.size})
    aux_sql= conteo
    f_FCR_ante= f1.filtro(aux_sql,db,fcr,fecha_ante,grupos_f,'FCR','ESTADO','VALORES')
#    f_FCR = resultado.sort_values(['FCR'], ascending=True).groupby(['FCR', 'ESTADO']).agg({'ESTADO': np.size})
    sqlt = consulta + " " + fecha_ante
    res = pd.read_sql(sqlt,db,index_col=None)
    res.loc[res['AREA'].isnull(), 'AREA'] = 'Blank'
    res.loc[res['FCR'].isnull(), 'FCR'] = 'Blank'
    f_est_ante = res.groupby('ESTADO').size()
#    f_est_ante= pd.DataFrame(f_est_ante)
    f_est_ante= f1.reordena(f_est_ante,'Estado','Valor','SR','Estado','Valor')
#    print('Cifras dia anterior completos...')
    lg.escribe_log('Cifras dia anterior completos...')
    lg.escribe_log('**Consulta datos FCR,FOLIOS,BACKLOG, PROMEDIO_SOLUCION ...')
    FCR_e = pd.read_sql(c_porcentaje,db,index_col=None)
    folios_e = pd.read_sql(c_folios,db,index_col=None)
    backlog_e = pd.read_sql(c_backlog,db,index_col=None) 
    
    c_promedio_aux=c_promedio.replace('VARIABLE',c_pro1)     
    prom_s_e1 = pd.read_sql(c_promedio_aux,db,index_col=None)
    c_promedio_aux=c_promedio.replace('VARIABLE',c_pro2)
    prom_s_e2 = pd.read_sql(c_promedio_aux,db,index_col=None)
    
    backlog_e = backlog_e.pivot(index='INS_PRODUCT', columns='SR_STAT_ID')['TOTAL']
    prom_s_e1 = prom_s_e1.pivot(index='AREA', columns='MES', values ='DIAS_SOL')
    prom_s_e2 = prom_s_e2.pivot(index='AREA', columns='MES', values ='DIAS_CLOSE')
    
    lg.escribe_log('El archivo se deposita en la carpeta '+carpeta+' ...')
    cfile.escribeExcel(var_fecha,'Cifras_Acum','Cifras_DAnterior','FCR','Case Age','BackLog','MTTR',resultado,f_est,f_FCR,f_areas,f_est_ante,f_FCR_ante,f_areas_ante,FCR_e,folios_e,backlog_e,prom_s_e1,prom_s_e2)
#    cfile.escribeExcel('pba_env','Cifras_Acum','Cifras_DAnterior',resultado,f_est,f_FCR,f_areas,f_est_ante,f_FCR_ante,f_areas_ante)
#    mimail.envia_mail('Prueba reporte SR 1er version '+var_fecha,"Se envio desde correo personal por la doble autenticacion del correo de Liverpool",'reporte_'+var_fecha+'.xlsx')
#    cftp.carga_Archivo(ip_ftp,user_ftp,pass_ftp,dir_ftp,'reporte_temp.xlsx','reporte_'+var_fecha+'.xlsx')
    fileup='reporte_'+var_fecha+'.xlsx'
#    print('Subiendo archivo a FTP'+fileup+'...')
    lg.escribe_log('Subiendo archivo a FTP '+fileup+'...')
    cftp.carga_Archivo(carpeta,fileup,fileup)
    con.close_conn
    depura.depura_Archivos(carpeta);
    
except Exception as inst:
#    print('ERROR:',inst)
    lg.escribe_log('ERROR'+str(inst)+'...')

#print("Termino...")
lg.escribe_log('Termino...')
