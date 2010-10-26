#!/usr/bin/python
# -*- coding: utf-8 -*-

from exercise01 import ProcesadorDeNombres

C = ProcesadorDeNombres('Jennifer','Maldonado')

print C.getDato('Nombre')

print C.setDato('Nombre','Daniel')

print C.setDato('Nombre','Angelito')

print C.setDato('apellido','Peña')

print C.getDato('Nombre')

print C.getDato('Apellido')

print C.setDato2({'nombre':'Jennifer','apellido':'Velasquez'})

print C.getDato('nombre')

print C.getDato('apellido')

#ejercicio 2.

from exercise02 import vehiculo

V = vehiculo()

V.encender()
V.acelerar()
V.frenar()
V.apagar()

V.acelerar()
V.encender()
V.frenar()
V.acelerar()
V.apagar()

from exercise03 import utility

#a = vehiculo()
U = utility()
U.prinattr()

U.updownvidrios()
U.onoffradio()
U.onofflimpiaparabrizas()

U.prinattr()

from exercise04 import age

age = age()

age.setedad(30)

print (age.getedad())

print age.verifyedad10()

print age.verifyedad60()

print age.verifyedad40()

print age.verifyedad20()
