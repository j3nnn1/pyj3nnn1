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

   def getedad(self):
      return self.edad 

   def verifyedad10(self):
      if self.edad>=0 and self.edad<10:
         result=True
      else:
	 result=False
      return result

   def verifyedad20(self):
      if self.edad>10 and self.edad<20:
         result=True
      else:
         result=False
      return result

   def verifyedad40(self):
      if self.edad>20 and self.edad<40:
         result=True
      else:
         result=False
      return result


   def verifyedad60(self):
      if self.edad>40 and self.edad<60:
         result=True
      else:
         result=False
      return result

   def verifyedadmore60(self):
      if self.edad>=60:
         result=True
      else:
         result=False
      return result

