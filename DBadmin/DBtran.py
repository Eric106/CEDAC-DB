# -*- coding: utf-8 -*-
import pyodbc 
import pandas as pd
import datetime as date
from tabulate import tabulate

cnxn = pyodbc.connect("Driver={SQL Server};Server=itesm.database.windows.net;Database=CEDAC-DB;uid=karla;pwd=Da19442500")
cursor = cnxn.cursor()
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(encoding='utf-8')

def lastRegTable(tabla,campo):
    table=pd.read_sql_query("select * from "+str(tabla)+" where "+str(tabla)+"."+str(campo)+" = (select max(t."+str(campo)+") from "+str(tabla)+" t)",cnxn)
    lista=str(table).split()
    return lista

def getNombrefromId(idAlumno):
    table=pd.read_sql_query("select nombre from alumno where idAlumno="+str(idAlumno),cnxn)
    usrName=str(table).split()[2]
    return str(usrName)

def gruposDisp():
    lista=[]
    table=pd.read_sql_query("select distinct grupo from alumno ",cnxn)
    if str(table).split()[0]=='Empty':
        return tuple(lista)
    else:
        for i in str(table).split()[1:]:
            if not i in '0123456789':
                lista.append(i)
        return tuple(lista)

def verAlumnosPorGrupo(grupo):
    table=pd.read_sql_query("select * from alumno where grupo='"+str(grupo)+"'",cnxn)
    if str(table).split()[0] == 'Empty':
        return 'No hay alumnos registrados'
    else:
        return str(tabulate(table,headers='keys',tablefmt='fancy_grid'))

def verAlumnos(nombre):
    table=pd.DataFrame()
    if nombre.isalpha():
        table=pd.read_sql_query("select * from alumno where nombre='"+str(nombre)+"'",cnxn)
    elif nombre.isdigit():
        table=pd.read_sql_query("select * from alumno where idAlumno="+str(nombre),cnxn)
    elif nombre=='':
        table=pd.read_sql_query("select * from alumno",cnxn)
    if str(table).split()[0] == 'Empty':
        return 'No hay alumnos registrados'
    else:
        return str(tabulate(table,headers='keys',tablefmt='fancy_grid'))

def agregarAlumnos(nombre,grupo,telefono):
    usrNewID=0
    if verAlumnos('') == 'No hay alumnos registrados':
        usrNewID=1
    else:
        usrNewID=int(lastRegTable('alumno','idAlumno')[5])+1
    usrName=nombre
    usrGrupo=grupo
    usrTel=telefono
    cursor.execute("insert into alumno values("+str(usrNewID)+", '"+str(usrName)+"','"+str(usrGrupo)+"','"+str(usrTel)+"' )")
    cnxn.commit()

def verActReg(nombre,dataFlag):
    table=pd.DataFrame()
    if dataFlag==0 and nombre.isalpha():
        table=pd.read_sql_query("select a.nombre, ac.nombreAct, e.periodo, e.A_pagar from estudiante_actividad e, alumno a, actividades ac where a.idAlumno=e.IDalumno and e.actividad=ac.idActividad and a.nombre='"+str(nombre)+"'",cnxn)
    elif dataFlag==1 and nombre.isalpha():
        table=pd.read_sql_query("select a.nombre, ac.nombreAct, e.periodo, e.A_pagar from estudiante_actividad e, alumno a, actividades ac where a.idAlumno=e.IDalumno and e.actividad=ac.idActividad and ac.nombreAct='"+str(nombre)+"'",cnxn)
    elif dataFlag==2 and nombre=='':
        table=pd.read_sql_query("select a.nombre, ac.nombreAct, e.periodo, e.A_pagar from estudiante_actividad e, alumno a, actividades ac where a.idAlumno=e.IDalumno and e.actividad=ac.idActividad",cnxn)
    if str(table).split()[0] == 'Empty':
        return 'No hay inscripciones registradas!!'
    else:
        return str(tabulate(table,headers='keys',tablefmt='fancy_grid'))

def actividadesDisp():
    lista=[]
    table=pd.read_sql_query("select nombreAct from actividades",cnxn)
    if str(table).split()[0]=='Empty':
        return tuple(lista)
    else:
        for i in str(table).split()[1:]:
            if not i in '0123456789':
                lista.append(i)
        return tuple(lista)

def alumnoExist(nombre):
    table=pd.read_sql_query("select nombre from alumno where nombre='"+str(nombre)+"'",cnxn) 
    if str(table).split()[0]=='Empty':
        return False
    else:
        return True

def dosActPeriodo(nombre):
    usrName=nombre
    idUsrTable=pd.read_sql_query("select idAlumno from alumno where nombre='"+str(usrName)+"'",cnxn)
    idUsr=str(idUsrTable).split()[2]
    fecha=str(date.datetime.now()).split()[0]
    año1=fecha[0:4]
    año2=''
    mes=fecha[5:7]
    periodo=''
    if mes in ['07','08','09','10','11','12']:
        año2=str(int(año1)+1)
        periodo=año1+'-'+año2
    elif mes in ['01','02','03','04','05','06']:
        año2=str(int(año1)-1)
        periodo=año2+'-'+año1
    #periodo='2017-2018' #BORRAR
    table=pd.read_sql_query("select count(*) from estudiante_actividad where IDalumno="+str(idUsr)+" and periodo='"+str(periodo)+"'",cnxn)
    numAct=int(str(table).split()[1])
    return numAct

def validateRegAct(nombre,actividad):
    usrName=nombre
    idUsrTable=pd.read_sql_query("select idAlumno from alumno where nombre='"+str(usrName)+"'",cnxn)
    idUsr=str(idUsrTable).split()[2]
    nameAct=actividad
    costoActTable=pd.read_sql_query("select idActividad, costo from actividades where nombreAct='"+str(nameAct)+"'",cnxn)
    costoAct=str(costoActTable).split()[4]
    idAct=str(costoActTable).split()[3]
    fecha=str(date.datetime.now()).split()[0]
    año1=fecha[0:4]
    año2=''
    mes=fecha[5:7]
    periodo=''
    if mes in ['07','08','09','10','11','12']:
        año2=str(int(año1)+1)
        periodo=año1+'-'+año2
    elif mes in ['01','02','03','04','05','06']:
        año2=str(int(año1)-1)
        periodo=año2+'-'+año1
    #periodo='2017-2018' #BORRAR
    listaAgreg=[idUsr,idAct,periodo,costoAct]
    table=pd.read_sql_query("select * from estudiante_actividad where IDalumno="+str(idUsr)+" and actividad="+str(idAct)+" and periodo='"+str(periodo)+"'",cnxn)
    if listaAgreg==(str(table).split()[5:9]):
        return False
    else:
        return True

def agregarRegAct(nombre,actividad):
    usrName=nombre
    idUsrTable=pd.read_sql_query("select idAlumno from alumno where nombre='"+str(usrName)+"'",cnxn)
    idUsr=str(idUsrTable).split()[2]
    nameAct=actividad
    costoActTable=pd.read_sql_query("select idActividad, costo from actividades where nombreAct='"+str(nameAct)+"'",cnxn)
    costoAct=str(costoActTable).split()[4]
    idAct=str(costoActTable).split()[3]
    fecha=str(date.datetime.now()).split()[0]
    año1=fecha[0:4]
    año2=''
    mes=fecha[5:7]
    periodo=''
    if mes in ['07','08','09','10','11','12']:
        año2=str(int(año1)+1)
        periodo=año1+'-'+año2
    elif mes in ['01','02','03','04','05','06']:
        año2=str(int(año1)-1)
        periodo=año2+'-'+año1
    #periodo='2017-2018' #BORRAR
    cursor.execute("insert into estudiante_actividad values("+str(idUsr)+","+str(idAct)+",'"+str(periodo)+"',"+str(costoAct)+")")
    cnxn.commit()

def getFillDataAdeud(nombre):
    lista=[[],[]]
    if verAdeudAlum(nombre)=='Alumno sin adeudos!!':
        return lista
    tableAct=pd.read_sql_query("select ac.nombreAct from estudiante_actividad e, actividades ac, alumno a where a.idAlumno=e.IDalumno and ac.idActividad=e.actividad and a.nombre='"+str(nombre)+"' and e.A_pagar>0",cnxn)
    tablePer=pd.read_sql_query("select e.periodo from estudiante_actividad e, actividades ac, alumno a where a.idAlumno=e.IDalumno and ac.idActividad=e.actividad and a.nombre='"+str(nombre)+"' and e.A_pagar>0",cnxn)
    lista1=str(tableAct).split()[1:]
    lista2=str(tablePer).split()[1:]
    for i in range(len(lista1)):
        if i%2!=0:
            lista[0].append(lista1[i])
            lista[1].append(lista2[i])
    listaTemp=[]
    for i in lista[0]:
        if i not in listaTemp:
            listaTemp.append(i)
    lista.pop(0)
    lista.insert(0,listaTemp)
    listaTemp=[]
    for i in lista[1]:
        if i not in listaTemp:
            listaTemp.append(i)
    lista.pop(1)
    lista.insert(1,listaTemp)
    listaTemp=[]
    return lista

def verAdeudAlum(nombre):
    table=pd.read_sql_query("select ac.nombreAct,e.periodo,e.A_pagar from estudiante_actividad e, actividades ac, alumno a where a.idAlumno=e.IDalumno and ac.idActividad=e.actividad and a.nombre='"+str(nombre)+"' and e.A_pagar>0",cnxn)
    if str(table).split()[0]=='Empty':
        return 'Alumno sin adeudos!!'
    else:
        return str(tabulate(table,headers='keys',tablefmt='fancy_grid'))

def validatePago(nombre,actividad,periodo,monto):
    usrName=nombre
    idUsrTable=pd.read_sql_query("select idAlumno from alumno where nombre='"+str(usrName)+"'",cnxn)
    idUsr=str(idUsrTable).split()[2]
    nameAct=actividad
    costoActTable=pd.read_sql_query("select idActividad from actividades where nombreAct='"+str(nameAct)+"'",cnxn)
    idAct=str(costoActTable).split()[2]
    table=pd.read_sql_query("select * from estudiante_actividad where IDalumno="+str(idUsr)+" and actividad="+str(idAct)+" and periodo='"+str(periodo)+"'",cnxn)
    regAct=str(table).split()[5:]
    if str(table).split()[0]=='Empty':
        return False
    elif float(regAct[3])-float(monto)<0:
        return False
    elif regAct[0:3]!=[idUsr,idAct,periodo]:
        return False
    else:
        return True

def pagarAct(nombre,actividad,periodo,monto):
    fecha=str(date.datetime.now()).split(' ')[0]
    folio=0
    if lastRegTable('pago','folio')[0]=='Empty':
        folio=1
    else:
        folio=int(lastRegTable('pago','folio')[6])+1
    usrName=nombre
    idUsrTable=pd.read_sql_query("select idAlumno from alumno where nombre='"+str(usrName)+"'",cnxn)
    idUsr=str(idUsrTable).split()[2]
    nameAct=actividad
    costoActTable=pd.read_sql_query("select idActividad from actividades where nombreAct='"+str(nameAct)+"'",cnxn)
    idAct=str(costoActTable).split()[2]
    cursor.execute("insert into pago values("+str(folio)+","+str(idUsr)+","+str(idAct)+","+str(monto)+",'"+str(fecha)+"')")
    cursor.execute("update estudiante_actividad set A_pagar=A_pagar-"+str(monto)+" where IDalumno="+str(idUsr)+" and actividad="+str(idAct)+" and periodo='"+str(periodo)+"'")
    cursor.commit()

def getNombre(folio):
    usrNameTable=pd.read_sql_query("select a.nombre from pago p, alumno a where p.estudiante=a.idAlumno and p.folio="+str(folio),cnxn)
    usrName=str(usrNameTable).split()[2]
    return str(usrName)

def verPagos(nombre):
    table=pd.DataFrame()
    if nombre.isalpha():
        table=pd.read_sql_query("select p.folio, ac.nombreAct,p.monto,p.fecha from pago p, alumno a, actividades ac where p.estudiante=a.idAlumno and p.idActividad=ac.idActividad and a.nombre='"+str(nombre)+"'",cnxn)
    elif nombre.isdigit():
        table=pd.read_sql_query("select p.folio, ac.nombreAct,p.monto,p.fecha from pago p, alumno a, actividades ac where p.estudiante=a.idAlumno and p.idActividad=ac.idActividad and p.folio="+str(nombre),cnxn)
    elif nombre=='':
        table=pd.read_sql_query("select p.folio, a.nombre,ac.nombreAct,p.monto,p.fecha from pago p, alumno a, actividades ac where p.estudiante=a.idAlumno and p.idActividad=ac.idActividad",cnxn)
    if str(table).split()[0]=='Empty':
        return 'No hay pagos existentes!!'
    else:
        return str(tabulate(table,headers='keys',tablefmt='fancy_grid'))

def verActividades(actividadNom):
    table=pd.DataFrame()
    if actividadNom=='':
        table=pd.read_sql_query("select * from actividades",cnxn)
    else:
        table=pd.read_sql_query("select * from actividades where nombreAct='"+str(actividadNom)+"'",cnxn)
    if str(table).split()[0]=='Empty':
        return 'No hay actividades registradas!!'
    else:
        return str(tabulate(table,headers='keys',tablefmt='fancy_grid'))

def agregarActividad(actividadNom,costoAct):
    newID=0
    if verActividades('')=='No hay actividades registradas!!':
        newID=1
    else:
        newID=int(lastRegTable('actividades','idActividad')[4])+1
    actividad=actividadNom
    costo=costoAct
    cursor.execute("insert into actividades values("+str(newID)+",'"+str(actividad)+"',"+str(costo)+")")
    cursor.commit()
