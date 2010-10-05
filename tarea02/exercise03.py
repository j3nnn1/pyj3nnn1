#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
3- Crear una subclase de Vehiculo que agregue al menos 3 funcionalidades adicionales como por ejemplo:
- Subir los vidrios
- Encender radio
- Usar los limpiaparabrizas
-- La clase debe ser inteligente y contener metodos de encendido y apagado
"""
from exercise02 import vehiculo

class utility(vehiculo):

    def __init__(self):
	vehiculo.__init__(self)
        self.vidriosarriba     = 1 
        self.radioOn           = 0
        self.limpiaparabrizaOn = 0

    def updownvidrios(self):
        if self.vidriosarriba:       
            self.vidriosarriba=0
        else: 
            self.vidriosarriba=1
    def onoffradio(self):
        if self.radioOn:
            self.radioOn=0
        else:
            self.radioOn=1

    def onofflimpiaparabrizas(self):
        if self.limpiaparabrizaOn:
            self.limpiaparabrizaOn =0 
        else:
	    self.limpiaparabrizaOn =1

    def prinattr(self):
        print 'Estado de la Radio: ' + str(self.radioOn)
        print 'Estado del limpiaparabriza: ' + str(self.limpiaparabrizaOn)
        print 'Estado del vidrio ' +str(self.vidriosarriba)


b = utility()
b.prinattr()
print 'Cambios'
b.onofflimpiaparabrizas()
b.onoffradio()
b.prinattr()
