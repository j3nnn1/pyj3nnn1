#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
1- Crear una clase llamada ProcesadorDeNombres
que requiera el nombre y el apellido y con los 
metodos set y get, obtenerlos y modificarlos
"""

class ProcesadorDeNombres:
    def __init__(self, nombre='', apellido=''):
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

