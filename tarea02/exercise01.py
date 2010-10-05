#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
1- Crear una clase llamada ProcesadorDeNombres
que requiera el nombre y el apellido y con los 
metodos set y get, obtenerlos y modificarlos
"""
class ProcesadorDeNombres:

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def getnombre(self):
        return self.nombre

    def setnombre(self, nombre):
        self.nombre = nombre
        return True

    def getapellido(self):
        return self.apellido

    def setapellido(self, apellido):
        self.apellido=apellido
        return True

    def getDato(self, *dato):
	if dato[0].lower()=='apellido':
	    result = self.apellido
	elif dato[0].lower()=='nombre':
	    result = self.nombre
	else:
	    result = None
        return result

    def setDato(self, *dato):
	if (len(dato)% 2)==0:
	    for cont, value in (enumerate(dato)):
                if value.lower()=='apellido':
		    self.apellido = dato[cont+1]
		elif value.lower()=='nombre':
		    self.nombre = dato[cont+1]
	else:
	   result = 'Debe ingresar parametros pares, Nombre, valor.'    	

    def setDato2(self, dato):
       return dato
       for ll,v in (dato):
            if ll.lower()=='nombre':
                self.nombre = v
            elif ll.lower()=='apellido':            
                self.apellido = v

