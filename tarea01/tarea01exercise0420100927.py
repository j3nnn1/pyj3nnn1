#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
4- Crear un script que pregunte el nombre, direccion y ciudad, concatenarlos y asegurarnos que cada uno de esos valores tenga la primera letra mayuscula
"""

def todoquestions():

   name      = raw_input("¿Cuál es tu nombre completo? ").capitalize();
   direccion = raw_input("¿Cuál es tu direccion? ").capitalize();
   city      = raw_input("¿Cuál es tu Ciudad? ").capitalize();

   return name +' '+direccion+' '+city; 


print todoquestions();

