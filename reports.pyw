# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import DBadmin.DBreport as db

def loadActIns():
    if len(db.datainscriPorAct())==0:
        messagebox.showerror("Error","no hay datos que graficar!!")
    else:
        lst=db.datainscriPorAct()
        db.plot(lst[0],lst[1],'Alumnos por actividad','Actividades','Alumnos')

def loadActIngre():
    if len(db.dataIngreAct())==0:
        messagebox.showerror("Error","no hay datos que graficar!!")
    else:
        lst=db.dataIngreAct()
        db.plot(lst[0],lst[1],'Ingresos por actividad','Actividades','Ingresos')

def loadCostoAct():
    if len(db.dataCostoAct())==0:
        messagebox.showerror("Error","no hay datos que graficar!!")
    else:
        lst=db.dataCostoAct()
        db.plot(lst[0],lst[1],'Costo por actividad','Actividades','Costos')

def mainFrame(window):
    frame=ttk.Frame(window,style='My.TFrame')
    frame.pack(fill='both',expand='yes')
    exitBtn=tk.Button(window,bg="#D9291E",fg=colorletra,command=exit,text="Salir",font=('30'))
    infoLab=tk.Label(window,text="                                      RESÚMENES                                      ",bg="#4F5150",fg=colorletra,font=('30'))
    actInsBtn=tk.Button(window,bg="#2CAB60",fg=colorletra,text="       Alumnos por actividad       ",font=('30'),command=loadActIns)
    ingreActBtn=tk.Button(window,bg="#2CAB60",fg=colorletra,text="       Ingresos por actividad       ",font=('30'),command=loadActIngre)
    costoActiBtn=tk.Button(window,bg="#2CAB60",fg=colorletra,text="         Costo por actividad         ",font=('30'),command=loadCostoAct)
    exitBtn.place(x=570,y=280)
    infoLab.place(x=120,y=50)
    actInsBtn.place(x=215,y=100)
    ingreActBtn.place(x=215,y=150)
    costoActiBtn.place(x=215,y=200)

rootWindow=tk.Tk()
rootWindow.geometry("640x360")
rootWindow.resizable('False','False')
rootWindow.title("CEDAC reportes clases extra-escolares")
rootWindow.iconbitmap(default="./assets/CEDAC.ico")
stilo=ttk.Style()
colorfondo='#251EC6'
colorletra='#FFFFFF'
stilo.configure('My.TFrame', background=colorfondo, foreground=colorletra)
mainFrame(rootWindow)
rootWindow.mainloop()