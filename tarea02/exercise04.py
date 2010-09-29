#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
4- Crear una clase que procese la edad de una persona 
y a traves de metodos verifique, retornando booleanos,
 si pertenece a estos grupos de edad y ademas, pueda ser
 modificada y luego revisar otra vez
- 0 a 10
- 11 a 20
- 21 a 40
- 41 a 60
- Mayor de 60
"""

class age:
   def __init__(self,edad=0):
      self.edad=edad

   def setedad(self,edad): 
      self.edad=edad
      return True

   def getedad(self,edad):
      return self.edad 

   def verifyedad10(self,edad):
      if edad>=0 and edad<10:
         result=True
      else:
	 result=False
      return result

   def verifyedad20(self,edad):
      if edad>10 and edad<20:
         result=True
      else:
         result=False
      return result

   def verifyedad40(self,edad):
      if edad>20 and edad<40:
         result=True
      else:
         result=False
      return result


   def verifyedad60(self,edad):
      if edad>40 and edad<60:
         result=True
      else:
         result=False
      return result

   def verifyedadmore60(self,edad):
      if edad>=60:
         result=True
      else:
         result=False
      return result

