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


