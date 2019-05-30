# -*- coding: utf-8 -*-
import pyodbc 
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

cnxn = pyodbc.connect("Driver={SQL Server};Server=itesm.database.windows.net;Database=CEDAC-DB;uid=karla;pwd=Da19442500")
cursor = cnxn.cursor()
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(encoding='utf-8')

def datainscriPorAct():
    actiDF=pd.read_sql_query("select ac.nombreAct from estudiante_actividad e, actividades ac where e.actividad=ac.idActividad group by ac.nombreAct",cnxn)
    inscriDF=pd.read_sql_query("select count(*) as inscritos from estudiante_actividad e, actividades ac where e.actividad=ac.idActividad group by ac.nombreAct",cnxn)
    if str(actiDF).split()[0]=='Empty':
        return []
    else:
        acti=clean1Column(str(actiDF).split()[1:])
        inscri=clean1Column(str(inscriDF).split()[1:])
        for i in range(len(inscri)):
            inscri[i]=int(inscri[i])
        return [acti,inscri]

def dataIngreAct():
    actiDF=pd.read_sql_query("select ac.nombreAct from pago p, actividades ac where p.idActividad=ac.idActividad group by ac.nombreAct",cnxn)
    ingreDF=pd.read_sql_query("select sum(monto) as ingresos from pago p, actividades ac where p.idActividad=ac.idActividad group by ac.nombreAct",cnxn)
    if str(actiDF).split()[0]=='Empty':
        return[]
    else:
        acti=clean1Column(str(actiDF).split()[1:])
        ingre=clean1Column(str(ingreDF).split()[1:])
        for i in range(len(ingre)):
            ingre[i]=float(ingre[i])
        return [acti,ingre]

def dataCostoAct():
    actiDF=pd.read_sql_query("select nombreAct from actividades",cnxn)
    costoDF=pd.read_sql_query("select costo from actividades",cnxn)
    if str(actiDF).split()[0]=='Empty':
        return[]
    else:
        acti=clean1Column(str(actiDF).split()[1:])
        costo=clean1Column(str(costoDF).split()[1:])
        for i in range(len(costo)):
            costo[i]=float(costo[i])
        return [acti,costo]
        
def plot(x,y,title,xlabel,ylabel):
    plt.bar(x,y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def clean1Column(lista):
    lst=[]
    for i in range(len(lista)):
        if i%2!=0:
            lst.append(lista[i])
    return lst
#inscriPorAct()