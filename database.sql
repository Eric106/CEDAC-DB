/*create database CEDAC
use CEDAC-DB*/

create table alumno
(
    idAlumno int,
    nombre varchar(50),
    grupo varchar(50),
    telefono varchar(50),
    constraint alumno_pk primary key(idAlumno)
);

create table actividades
(
    idActividad int,
    nombreAct varchar(50),
    costo float,
    constraint actividad_pk primary key(idActividad)
);

create table pago
(
    folio int,
    estudiante int,
	idActividad int,
    monto float,
    fecha date,
    constraint pago_pk primary key(folio, estudiante),
    constraint pago_fkEst foreign key(estudiante) references alumno(idAlumno)
);

create table estudiante_actividad
(
    IDalumno int,
    actividad int,
    periodo varchar(50),
    A_pagar float,
    constraint estAct_pk primary key (IDalumno, actividad, periodo),
    constraint estAct_fkEst foreign key(IDalumno) references alumno(idAlumno),
    constraint estAct_fkAct foreign key(actividad) references actividades(idActividad)
);

insert into alumno
values(1, 'Erick', 'Clase F', '5529495870')
insert into alumno
values(2, 'Eric', 'Clase F', '5529495870')
insert into alumno
values(3, 'Karla', 'Grupo A', '5549085678')
insert into alumno
values(4, 'Rafa', 'Grupo P', '5548211241')

insert into actividades
values(1, 'Natacion', 300)
insert into actividades
values(2, 'Futbol', 200)
insert into actividades
values(3, 'Basquetball', 250)

insert into estudiante_actividad values(3,1,'2018-2019', 300)
insert into pago values(1,3,1,100.0,'2018-10-30')
update estudiante_actividad set A_pagar=A_pagar-100.0 where IDalumno=3