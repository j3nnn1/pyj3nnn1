#!/usr/bin/python
# -*- coding: utf-8 -*-
# j3nnn1

"""
2- Crear la clase Vehiculo con los metodos encender, apagar, acelerar y frenar. La clase debe ser lo suficientemente inteligente para que sepa que no puede:
- Apagar sin estar encendido
- Frenar sin estar acelerando 
- Encender sin estar apagado
- Acelerar si no esta detenido
"""

class vehiculo:
    def __init__(self):
        self.encendido    =0
        self.detenido     =1

    def encender(self):
        if self.encendido:
           print 'No se puede encender, ups Vehículo ya está encendido'
        else:
           self.encendido =1

    def apagar(self):
        if self.encendido==0:
           print 'No se puede apagar, ups Vehículo ya esta apagado!!'
        else:
            self.encendido=0

    def acelerar(self):
        if self.detenido==0 or self.encendido==0:
           print 'No se puede acelerar, ups Vehículo ya esta acelerando o esta apagado'
        else:
            self.detenido=0

    def frenar(self):
        if self.detenido or self.encendido==0:
           print 'No se puede frenar, wow Vehículo esta detenido!'
        else:
            self.detenido=1


