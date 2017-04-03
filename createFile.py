# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 17:06:35 2016

@author: edejc
"""

import pandas as pd
import escribe_log as lg
import xlsxwriter as xwrite
try:
    from ConfigParser import ConfigParser
except ImportError:
    # Python 3
    from configparser import ConfigParser
    
parametros = ConfigParser()
parametros.read("conf.cfg")
carpeta = parametros.get("CARPETA", "RUTA")

def escribeExcel(var_fecha,hoja1,hoja2,hoja3,hoja4,hoja5,hoja6,resultado,f_est,f_FCR,f_areas,f_est_ante,f_FCR_ante,f_areas_ante,FCR_e,folios_e,backlog_e,prom_s_e1,prom_s_e2):
    #    
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(carpeta+'reporte_'+var_fecha+'.xlsx', engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    resultado.to_excel(writer, sheet_name='Acumulado')
#    
    f_est.to_excel(writer, sheet_name=hoja1, startrow = 1, startcol = 2)
    f_FCR.to_excel(writer, sheet_name=hoja1,startrow = 6, startcol = 2)
    f_areas.to_excel(writer, sheet_name=hoja1,startrow = 13, startcol = 2)
    #
    f_est_ante.to_excel(writer, sheet_name=hoja2, startrow = 1, startcol = 2)
    f_FCR_ante.to_excel(writer, sheet_name=hoja2,startrow = 6, startcol = 2)
    f_areas_ante.to_excel(writer, sheet_name=hoja2,startrow =13, startcol = 2)
    
    FCR_e.to_excel(writer, sheet_name=hoja3, startrow = 1, startcol = 2)
    folios_e.to_excel(writer, sheet_name=hoja4,startrow = 1, startcol = 2)
    
    backlog_e.to_excel(writer, sheet_name=hoja5, startrow = 1, startcol = 2)
    
    prom_s_e1.to_excel(writer, sheet_name=hoja6,startrow = 2, startcol = 2)
    prom_s_e2.to_excel(writer, sheet_name=hoja6,startrow = 12, startcol = 2)    
    
#    backlog_e.to_excel(writer, sheet_name=hoja3,startrow = 1, startcol = 2)
	# Get the xlsxwriter objects from the dataframe writer object.
#    print('Datos en excel completo...')
    lg.escribe_log('Datos en excel completo...')
    formulas(hoja1,writer)
    formulas(hoja2,writer)
    formulas1(hoja4,writer)
    porcentajes(hoja3,writer)
    modificacion_titulos(hoja6,writer)
    writer.save()
    return()
    
def formulas(hoja,writer):
#    print('Calculando totales...')
    lg.escribe_log('Calculando totales...')
    worksheet = writer.sheets[hoja]
    worksheet.write('J2', 'Total')
    worksheet.write_formula('J3', '{=SUM(D3:I3)}')
    
    worksheet.write('J7', 'Total')
    for i in range(8,11):
        form='{=SUM(D' + (str(i))+':I'+(str(i))+')}'
        worksheet.write_formula(('J'+str(i)), form)
    
    worksheet.write('J14', 'Total')
    for i in range(15,23):
        form='{=SUM(D' + (str(i))+':I'+(str(i))+')}'
        worksheet.write_formula(('J'+str(i)), form)
    
    worksheet.write('C11', 'Gran Total')
    for i in "DEFGHIJ":
        var=('{=SUM('+i+'8:'+i+'10)}')
        worksheet.write_formula((i+'11'), var)
	
    worksheet.write('C23', 'Gran Total')
    for i in "DEFGHIJ":
        var=('{=SUM('+i+'15:'+i+'22)}')
        worksheet.write_formula((i+'23'), var)
    return()
    
def formulas1(hoja,writer):
#    print('Calculando totales...')
    lg.escribe_log('Calculando totales 2...')
    worksheet = writer.sheets[hoja]
    worksheet.write('E2', '0-5 Días')
    worksheet.write('F2', '6-15 Días')
    worksheet.write('G2', '16-30 Días')
    worksheet.write('H2', '>30 Días')
    worksheet.write('I2', 'Total')
    
    for i in range(3,9):
        form='{=SUM(E' + (str(i))+':H'+(str(i))+')}'
        worksheet.write_formula(('I'+str(i)), form)
    
    return()

def porcentajes(hoja,writer):
#    print('Calculando totales...')
#    format = workbook.add_format()
#
#    format.set_pattern(1)  # This is optional when using a solid fill.
#    format.set_bg_color('green')
    lg.escribe_log('Calculando porcentajes ...')
    worksheet = writer.sheets[hoja]
    worksheet.write('D2', 'CAMPAÑA')
    worksheet.write('H2', '%FCR')
    
    for i in range(3,27):
        form='{=ROUND(((F'+str(i)+'*100)/G'+str(i)+'),2)}'
        worksheet.write_formula(('H'+str(i)), form)
#        worksheet.write('A1', 'Ray', format)  
        
    return()

def modificacion_titulos(hoja,writer):
    worksheet = writer.sheets[hoja]
    worksheet.write('B2', 'TIEMPO PROMEDIO DE SOLUCION')
    worksheet.write('B12', 'TIEMPO PROMEDIO DE CIERRE')
    return()