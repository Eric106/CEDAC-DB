# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import DBadmin.DBtran as db

def reloadAlumnos(cTexto,nombre,dataFlag,comboBox):
    tabla=''
    if dataFlag==0 and nombre.get().isalpha() and nombre.get()!='':
        if db.alumnoExist(nombre.get()):
            tabla=db.verAlumnos(nombre.get())
            cTexto.config(state='normal')
            cTexto.delete('1.0','end')
            cTexto.insert('end','[ALUMNO/'+nombre.get().upper()+']\n'+tabla)
            cTexto.config(state='disabled')
        else:
            messagebox.showerror("Error de datos","El alumno no existe!!")
    elif dataFlag==1 and nombre.get().isdigit() and nombre.get()!='':
        tabla=db.verAlumnos(nombre.get())
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[ALUMNO/'+db.getNombrefromId(nombre.get()).upper()+']\n'+tabla)
        cTexto.config(state='disabled')
    elif dataFlag==2 and nombre.get()=='':
        tabla=db.verAlumnos(nombre.get())
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[ALUMNOS/TODOS]\n'+tabla)
        cTexto.config(state='disabled')
    elif dataFlag==3 and nombre.get()!='':
        tabla=db.verAlumnosPorGrupo(nombre.get())
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[ALUMNOS/GRUPO '+nombre.get().upper()+']\n'+tabla)
        cTexto.config(state='disabled')
    else:
        messagebox.showerror("Error de datos","Por nombre & Por grupo:[SOLO LETRAS]--Por ID:[SOLO NÚMEROS]")
    comboBox['values']=db.gruposDisp()
    comboBox.set('')
    nombre.set('')

def pesVerAlumnos(libro):
    nombre=tk.StringVar()
    idAlumno=tk.StringVar()
    pestañaVerAlumnos=ttk.Frame(libro,style='My.TFrame')
    libro.add(pestañaVerAlumnos,text='Ver Alumnos')
    tabla=db.verAlumnos('')
    cuadroTxt=tk.Text(pestañaVerAlumnos,width=77,height=10)
    cuadroTxt.insert('end','[ALUMNOS/TODOS]\n'+tabla)
    scroll=tk.Scrollbar(pestañaVerAlumnos,command=cuadroTxt.yview)
    cuadroTxt.config(state='disabled',yscrollcommand=scroll.set)
    exitBtn=tk.Button(pestañaVerAlumnos,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    infoLab=tk.Label(pestañaVerAlumnos,text='                          Tipos de búsqueda                          ',fg=colorletra,bg="#283747",font=('30'))
    nombreLab=tk.Label(pestañaVerAlumnos,text="Por nombre: ",fg=colorletra,bg=colorfondo,font=('20'))
    IDLab=tk.Label(pestañaVerAlumnos,text="Por ID: ",fg=colorletra,bg=colorfondo,font=('20'))
    comboGrupos=ttk.Combobox(pestañaVerAlumnos)
    cargarNombreBtn=tk.Button(pestañaVerAlumnos,bg="#16A085",fg=colorletra,command=lambda: reloadAlumnos(cuadroTxt,nombre,0,comboGrupos),text="Cargar",font=('30'))
    cargarIdBtn=tk.Button(pestañaVerAlumnos,bg="#16A085",fg=colorletra,command=lambda: reloadAlumnos(cuadroTxt,idAlumno,1,comboGrupos),text="Cargar",font=('30'))
    refreshBtn=tk.Button(pestañaVerAlumnos,bg="#25B4AC",fg=colorletra,command=lambda: reloadAlumnos(cuadroTxt,nombre,2,comboGrupos) ,text="Recargar",font=('30'))
    nombreEnt=tk.Entry(pestañaVerAlumnos,textvariable=nombre,width=23)
    idAlumnoEnt=tk.Entry(pestañaVerAlumnos,textvariable=idAlumno,width=23)
    grupoLab=tk.Label(pestañaVerAlumnos,text="Por grupo:",fg=colorletra,bg=colorfondo,font=('30'))
    cargarGrupoBtn=tk.Button(pestañaVerAlumnos,bg="#16A085",fg=colorletra,command=lambda: reloadAlumnos(cuadroTxt,comboGrupos,3,comboGrupos),text="Cargar",font=('30'))
    comboGrupos['values']=db.gruposDisp()
    cuadroTxt.grid(row=0,column=0)
    scroll.grid(row=0,column=1,sticky="nsew")
    exitBtn.place(x=570,y=280)
    refreshBtn.place(x=40,y=280)
    infoLab.place(x=150,y=170)
    nombreLab.place(x=182,y=205)
    IDLab.place(x=219,y=245)
    nombreEnt.place(x=275,y=205)
    idAlumnoEnt.place(x=275,y=245)
    cargarNombreBtn.place(x=420,y=200)
    cargarIdBtn.place(x=420,y=240)
    grupoLab.place(x=194,y=280)
    comboGrupos.place(x=275,y=282)
    cargarGrupoBtn.place(x=420,y=280)

def enviarAlumno(nombre,grupo,telefono):
    if (nombre.get()!='' and grupo.get()!='' and telefono.get()!=''):
        if db.alumnoExist(nombre.get()):
            messagebox.showerror('Error','Alumno ya registrado!!')
        else:
            db.agregarAlumnos(nombre.get(),grupo.get(),telefono.get())
            messagebox.showinfo("Mensaje","Alumno agregado exitosamente!!")
    else:
        messagebox.showerror("Error de datos","Datos incompletos")

    nombre.set("")
    grupo.set("")
    telefono.set("")

def pesAgregarAlumnos(libro):
    nombre=tk.StringVar()
    grupo=tk.StringVar()
    telefono=tk.StringVar()
    pestañaAgregarAlumnos=ttk.Frame(libro,style='My.TFrame')
    libro.add(pestañaAgregarAlumnos,text='Agregar Alumnos')
    nombreLab=tk.Label(pestañaAgregarAlumnos,text="Nombre: ",fg=colorletra,bg=colorfondo,font=('30'))
    grupoLab=tk.Label(pestañaAgregarAlumnos,text="Grupo: ",fg=colorletra,bg=colorfondo,font=('30'))
    telefonoLab=tk.Label(pestañaAgregarAlumnos,text="Teléfono: ",fg=colorletra,bg=colorfondo,font=('30'))
    nombreEnt=tk.Entry(pestañaAgregarAlumnos,textvariable=nombre)
    grupoEnt=tk.Entry(pestañaAgregarAlumnos,textvariable=grupo)
    telefonoEnt=tk.Entry(pestañaAgregarAlumnos,textvariable=telefono)
    exitBtn=tk.Button(pestañaAgregarAlumnos,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    enviarBtn=tk.Button(pestañaAgregarAlumnos,bg="#1C9553",fg=colorletra,command=lambda: enviarAlumno(nombre,grupo,telefono),text="Enviar",font=('30'))
    nombreLab.place(x=165,y=90)
    nombreEnt.place(x=250,y=90)
    grupoLab.place(x=177,y=120)
    grupoEnt.place(x=250,y=120)
    telefonoLab.place(x=160,y=150)
    telefonoEnt.place(x=250,y=150)
    exitBtn.place(x=570,y=280)
    enviarBtn.place(x=250,y=180)

def reloadInscri(cTexto,nombre,dataFlag,comboBox):
    tabla=''
    if dataFlag==0 and nombre.get()!='' and nombre.get().isalpha():
        if db.alumnoExist(nombre.get()):
            tabla=db.verActReg(nombre.get(),dataFlag)
            cTexto.config(state='normal')
            cTexto.delete('1.0','end')
            cTexto.insert('end','[INSCRIPCIONES/'+str(nombre.get().upper())+']\n'+tabla)
            cTexto.config(state='disabled')
        else:
            messagebox.showerror("Error de datos","El alumno no existe!!")
    elif dataFlag==1 and nombre.get()!='' and nombre.get().isalpha():
        tabla=db.verActReg(nombre.get(),dataFlag)
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[INSCRIPCIONES/'+str(nombre.get().upper())+']\n'+tabla)
        cTexto.config(state='disabled')
    elif dataFlag==2 and nombre.get()=='':
        tabla=db.verActReg(nombre.get(),dataFlag)
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[INSCRIPCIONES/TODAS]\n'+tabla)
        cTexto.config(state='disabled')
    else:
        messagebox.showerror("Error de datos","Por nombre & Por actividad:[SOLO LETRAS]")
    comboBox['values']=db.actividadesDisp()
    nombre.set('')
    comboBox.set('')

def pesVerInscri(libro):
    nombre=tk.StringVar()
    pestañaInscri=ttk.Frame(libro,style='My.TFrame')
    libro.add(pestañaInscri,text='Ver inscripciones')
    tabla=db.verActReg('',2)
    cuadroTxt=tk.Text(pestañaInscri,width=77,height=10)
    cuadroTxt.insert('end','[INSCRIPCIONES/TODAS]\n'+tabla)
    scroll=tk.Scrollbar(pestañaInscri,command=cuadroTxt.yview)
    cuadroTxt.config(state='disabled',yscrollcommand=scroll.set)
    exitBtn=tk.Button(pestañaInscri,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    infoLab=tk.Label(pestañaInscri,text='                          Tipos de búsqueda                          ',fg=colorletra,bg="#283747",font=('30'))
    nombreLab=tk.Label(pestañaInscri,text="Por nombre: ",fg=colorletra,bg=colorfondo,font=('20'))
    comboGrupos=ttk.Combobox(pestañaInscri)
    cargarNombreBtn=tk.Button(pestañaInscri,bg="#16A085",fg=colorletra,command=lambda: reloadInscri(cuadroTxt,nombre,0,comboGrupos),text="Cargar",font=('30'))
    cargarGrupoBtn=tk.Button(pestañaInscri,bg="#16A085",fg=colorletra,command=lambda: reloadInscri(cuadroTxt,comboGrupos,1,comboGrupos),text="Cargar",font=('30'))
    refreshBtn=tk.Button(pestañaInscri,bg="#25B4AC",fg=colorletra,command=lambda: reloadInscri(cuadroTxt,nombre,2,comboGrupos) ,text="Recargar",font=('30'))
    nombreEnt=tk.Entry(pestañaInscri,textvariable=nombre,width=23)
    grupoLab=tk.Label(pestañaInscri,text="Por actividad:",fg=colorletra,bg=colorfondo,font=('30'))
    comboGrupos['values']=db.actividadesDisp()
    cuadroTxt.grid(row=0,column=0)
    scroll.grid(row=0,column=1,sticky="nsew")
    exitBtn.place(x=570,y=280)
    refreshBtn.place(x=40,y=280)
    infoLab.place(x=150,y=170)
    nombreLab.place(x=182,y=205)
    nombreEnt.place(x=275,y=205)
    cargarNombreBtn.place(x=420,y=200)
    grupoLab.place(x=172,y=245)
    comboGrupos.place(x=275,y=247)
    cargarGrupoBtn.place(x=420,y=240)

def enviarRegAct(nombre,actividad):
    if(nombre.get()!='' and actividad.get()!=''):
        if db.alumnoExist(nombre.get()):
            if db.dosActPeriodo(nombre.get())<2:
                if db.validateRegAct(nombre.get(),actividad.get()):
                    db.agregarRegAct(nombre.get(),actividad.get())
                    messagebox.showinfo("Mensaje", "Alumno registrado en la actividad exitosamente!!!")
                else:
                    messagebox.showerror("Error registro","Alumno ya registrado en la actividad!! ")
            else:
                messagebox.showerror("Error registro","Solo se puede tener 2 actividades por periodo!!")
        else:
            messagebox.showerror("Error de datos","El alumno no existe!!")
    else:
        messagebox.showerror("Error de datos","Datos incompletos!!")
    nombre.set('')
    actividad.set('')

def pesinscribirActividad(libro):
    nombre=tk.StringVar()
    pestañaInscri=ttk.Frame(libro,style='My.TFrame')
    libro.add(pestañaInscri,text='Inscribir actividad')
    nombreLab=tk.Label(pestañaInscri,text="Nombre: ",fg=colorletra,bg=colorfondo,font=('30'))
    actividadLab=tk.Label(pestañaInscri,text="Actividad: ",fg=colorletra,bg=colorfondo,font=('30'))
    nombreEnt=tk.Entry(pestañaInscri,textvariable=nombre,width=23)
    actividadcombo=ttk.Combobox(pestañaInscri)
    actividadcombo['values']=db.actividadesDisp()
    exitBtn=tk.Button(pestañaInscri,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    enviarBtn=tk.Button(pestañaInscri,bg="#1C9553",fg=colorletra,command=lambda: enviarRegAct(nombre,actividadcombo),text="Enviar",font=('30'))
    nombreLab.place(x=165,y=90)
    nombreEnt.place(x=250,y=90)
    actividadLab.place(x=155,y=120)
    actividadcombo.place(x=250,y=120)
    exitBtn.place(x=570,y=280)
    enviarBtn.place(x=250,y=150)

def loadAdeud(nombre,cTexto,comboActividad,comboPeriodo):
    if nombre.get()!='':
        if db.alumnoExist(nombre.get()):
            tabla=db.verAdeudAlum(nombre.get())
            cTexto.config(state='normal')
            cTexto.delete('1.0','end')
            cTexto.insert('end','[Adeudos/'+str(nombre.get().upper())+']\n'+tabla)
            cTexto.config(state='disabled')
            comboActividad['values']=tuple(db.getFillDataAdeud(nombre.get())[0])
            comboPeriodo['values']=tuple(db.getFillDataAdeud(nombre.get())[1])
        else:
            messagebox.showerror("Error de datos","El alumno no existe!!")
    else:
        messagebox.showerror("Error de datos","Datos incompletos!!")

def enviarPago(nombre,actividad,periodo,monto):
    if nombre.get()!='' and actividad.get()!='' and periodo.get()!='' and monto.get()!='':
        if db.validatePago(nombre.get(),actividad.get(),periodo.get(),monto.get()):
            db.pagarAct(nombre.get(),actividad.get(),periodo.get(),monto.get())
            messagebox.showinfo("Mensaje","Actividad pagada con exito!!")
        else:
            messagebox.showerror("Error de datos","No se puede pagar, los datos son incorrectos!!")
    else:
        messagebox.showerror("Error de datos","Datos incompletos!!")
    actividad.set('')
    periodo.set('')
    monto.set('')

def pesPagarAct(libro):
    nombre=tk.StringVar()
    monto=tk.StringVar()
    pestañaPagar=ttk.Frame(libro,style='My.TFrame')
    libro.add(pestañaPagar,text='Pagar actividad')
    cuadroTxt=tk.Text(pestañaPagar,width=50,height=10)
    cuadroTxt.insert('end','Ingrese un alumno + [Cargar] ------>')
    scroll=tk.Scrollbar(pestañaPagar,command=cuadroTxt.yview)
    cuadroTxt.config(state='disabled',yscrollcommand=scroll.set)
    nombreLab=tk.Label(pestañaPagar,text='Nombre: ',fg=colorletra,bg=colorfondo,font=('25'))
    nombreEnt=tk.Entry(pestañaPagar,textvariable=nombre)
    actividadLab=tk.Label(pestañaPagar,text="Actividad: ",fg=colorletra,bg=colorfondo,font=('30'))
    periodoLab=tk.Label(pestañaPagar,text="Periodo: ",fg=colorletra,bg=colorfondo,font=('30'))
    montoLab=tk.Label(pestañaPagar,text="Monto: ",fg=colorletra,bg=colorfondo,font=('30'))
    montoEnt=tk.Entry(pestañaPagar,textvariable=monto,width=23)
    comboActividad=ttk.Combobox(pestañaPagar)
    comboPeriodo=ttk.Combobox(pestañaPagar)
    cargarBtn=tk.Button(pestañaPagar,bg="#2E86C1",fg=colorletra,command=lambda: loadAdeud(nombre,cuadroTxt,comboActividad,comboPeriodo),text="Cargar",font=('30'))
    pagarBtn=tk.Button(pestañaPagar,bg="#1C9553",fg=colorletra,command=lambda: enviarPago(nombre,comboActividad,comboPeriodo,monto),text="Pagar",font=('30'))
    exitBtn=tk.Button(pestañaPagar,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    pagarLab=tk.Label(pestañaPagar,text="Complete los desplegables una vez ingresado el alumno",fg=colorletra,bg='#283747',font=('30'))
    cuadroTxt.grid(row=0,column=0)
    scroll.grid(row=0,column=1,sticky="nsew")
    nombreLab.place(x=430,y=50)
    nombreEnt.place(x=500,y=50)
    cargarBtn.place(x=500,y=80)
    pagarBtn.place(x=320,y=250)
    exitBtn.place(x=570,y=280)
    pagarLab.place(x=5,y=170)
    actividadLab.place(x=62,y=200)
    periodoLab.place(x=70,y=230)
    montoLab.place(x=82,y=260)
    comboActividad.place(x=150,y=200)
    comboPeriodo.place(x=150,y=230)
    montoEnt.place(x=150,y=260)
    
def reloadPagos(cTexto,nombre,dataFlag):
    tabla=db.verPagos(nombre.get())
    if dataFlag==0 and nombre.get().isalpha() and nombre.get()!='':
        if db.alumnoExist(nombre.get()):
            cTexto.config(state='normal')
            cTexto.delete('1.0','end')
            cTexto.insert('end','[Pagos/'+nombre.get().upper()+']\n'+tabla)
            cTexto.config(state='disabled')
        else:
            messagebox.showerror("Error de datos","El alumno no existe!!")
    elif dataFlag==1 and nombre.get().isdigit() and nombre.get()!='':
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[Pago/'+db.getNombre(nombre.get()).upper()+']\n'+tabla)
        cTexto.config(state='disabled')
    elif dataFlag==2 and nombre.get()=='':
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[Pagos/TODOS]\n'+tabla)
        cTexto.config(state='disabled')
    else:
        messagebox.showerror("Error de datos", "por nombre:[SOLO LETRAS]--por folio:[SOLO NÚMEROS]")
    nombre.set('')

def pesVerPagos(libro):
    nombre=tk.StringVar()
    folio=tk.StringVar()
    pestañaPagar=ttk.Frame(libro,style='My.TFrame')
    libro.add(pestañaPagar,text='Ver Pagos')
    tabla=db.verPagos(nombre.get())
    cuadroTxt=tk.Text(pestañaPagar,width=77,height=10)
    cuadroTxt.insert('end','[Pagos/TODOS]\n'+tabla)
    scroll=tk.Scrollbar(pestañaPagar,command=cuadroTxt.yview)
    cuadroTxt.config(state='disabled',yscrollcommand=scroll.set)
    exitBtn=tk.Button(pestañaPagar,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    infoLab=tk.Label(pestañaPagar,text='                          Tipos de búsqueda                          ',fg=colorletra,bg="#283747",font=('30'))
    nombreLab=tk.Label(pestañaPagar,text="Por nombre: ",fg=colorletra,bg=colorfondo,font=('20'))
    folioLab=tk.Label(pestañaPagar,text="Por folio de pago: ",fg=colorletra,bg=colorfondo,font=('20'))
    cargarNombreBtn=tk.Button(pestañaPagar,bg="#16A085",fg=colorletra,command=lambda: reloadPagos(cuadroTxt,nombre,0),text="Cargar",font=('30'))
    cargafolioBtn=tk.Button(pestañaPagar,bg="#16A085",fg=colorletra,command=lambda: reloadPagos(cuadroTxt,folio,1),text="Cargar",font=('30'))
    cargarTodoBtn=tk.Button(pestañaPagar,bg="#25B4AC",fg=colorletra,command=lambda: reloadPagos(cuadroTxt,nombre,2),text="Recargar",font=('30'))
    nombreEnt=tk.Entry(pestañaPagar,textvariable=nombre)
    idAlumnoEnt=tk.Entry(pestañaPagar,textvariable=folio)
    cuadroTxt.grid(row=0,column=0)
    scroll.grid(row=0,column=1,sticky="nsew")
    exitBtn.place(x=570,y=280)
    infoLab.place(x=150,y=170)
    nombreLab.place(x=191,y=205)
    folioLab.place(x=153,y=245)
    nombreEnt.place(x=290,y=205)
    idAlumnoEnt.place(x=290,y=245)
    cargarNombreBtn.place(x=420,y=200)
    cargafolioBtn.place(x=420,y=240)
    cargarTodoBtn.place(x=40,y=280)
    
def reloadActi(cTexto,ComboBox):
    tabla=''
    if  ComboBox.get() in list(db.actividadesDisp()):
        tabla=db.verActividades(ComboBox.get())
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[Actividad/'+str(ComboBox.get().upper())+']\n'+tabla)
        cTexto.config(state='disabled')
    elif ComboBox.get()=='':
        tabla=db.verActividades(ComboBox.get())
        cTexto.config(state='normal')
        cTexto.delete('1.0','end')
        cTexto.insert('end','[Actividades/TODAS]\n'+tabla)
        cTexto.config(state='disabled')
        ComboBox['values']=db.actividadesDisp()
    else:
        messagebox.showerror("Error de datos","Porfavor seleccione una opcion del ComboBox")
    ComboBox.set('')

def enviarActividad(actividad,costo):
    if actividad.get()!='' and costo.get()!='':
        if actividad.get().isalpha() and costo.get().isdigit():
            db.agregarActividad(actividad.get(),costo.get())
            messagebox.showinfo("Mensaje","Actividad guardada con exito!!")
        else:
            messagebox.showerror("Error de datos","Actividad:[SOLO LETRAS]--Costo:[SOLO NÚMEROS]")
    else:
        messagebox.showerror("Error de datos","Datos incompletos!!")
    actividad.set('')
    costo.set('')

def pesActividades(libro):
    actividad=tk.StringVar()
    costo=tk.StringVar()
    pestañaAct=ttk.Frame(libro,style='My.TFrame')
    libro.add(pestañaAct,text='Actividades')
    tabla=db.verActividades('')
    cuadroTxt=tk.Text(pestañaAct, width=77,height=10)
    cuadroTxt.insert('end','[Actividades/TODAS]\n'+tabla)
    scroll=tk.Scrollbar(pestañaAct,command=cuadroTxt.yview)
    cuadroTxt.config(state='disabled',yscrollcommand=scroll.set)
    exitBtn=tk.Button(pestañaAct,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    detallesLab=tk.Label(pestañaAct,text="Ver detalles de:                                      ",fg=colorletra,bg="#16A085",font=('30'))
    comboActividad=ttk.Combobox(pestañaAct)
    comboActividad['values']=db.actividadesDisp()
    buscarBtn=tk.Button(pestañaAct,bg="#16A085",fg=colorletra,command=lambda: reloadActi(cuadroTxt,comboActividad),text="Buscar")
    infoLab=tk.Label(pestañaAct,text="                              Agregar actividad                             ",fg=colorletra,bg="#283747",font=('30'))
    actividadLab=tk.Label(pestañaAct,text="Nombre actividad: ",fg=colorletra,bg=colorfondo,font=('30'))
    costoLab=tk.Label(pestañaAct,text="Costo actividad: ",fg=colorletra,bg=colorfondo,font=('30'))
    actividadEnt=tk.Entry(pestañaAct,textvariable=actividad,width=27)
    costoEnt=tk.Entry(pestañaAct,textvariable=costo,width=27)
    agregarBtn=tk.Button(pestañaAct,bg="#16A085",fg=colorletra,command=lambda: enviarActividad(actividad,costo),text="Agregar")
    todoBtn=tk.Button(pestañaAct,bg="#16A085",fg=colorletra,command=lambda: reloadActi(cuadroTxt,comboActividad),text="Cargar todas las actividades disponibles")
    cuadroTxt.grid(row=0,column=0)
    scroll.grid(row=0,column=1,sticky="nsew")
    exitBtn.place(x=570,y=280)
    detallesLab.place(x=10,y=270)
    comboActividad.place(x=125,y=272)
    buscarBtn.place(x=270,y=270)
    todoBtn.place(x=320,y=270)
    infoLab.place(x=100,y=170)
    actividadLab.place(x=100,y=200)
    costoLab.place(x=114,y=230)
    actividadEnt.place(x=240,y=200)
    costoEnt.place(x=240,y=230)
    agregarBtn.place(x=413,y=210)

rootWindow=tk.Tk()
rootWindow.geometry("640x360")
rootWindow.resizable('False','False')
rootWindow.title("CEDAC transacciones de clases extra-escolares")
rootWindow.iconbitmap(default="./assets/CEDAC.ico")
notebook=ttk.Notebook(rootWindow)
notebook.pack(fill='both',expand='yes')
stilo=ttk.Style()
colorfondo='#251EC6'
colorletra='#FFFFFF'
stilo.configure('My.TFrame', background=colorfondo, foreground=colorletra)
pesVerAlumnos(notebook)
pesAgregarAlumnos(notebook)
pesVerInscri(notebook)
pesinscribirActividad(notebook)
pesPagarAct(notebook)
pesVerPagos(notebook)
pesActividades(notebook)
rootWindow.mainloop()

