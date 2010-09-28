#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
7- Mejorar la última funcion que reciba un tercer parametro para definir la mayoria de edad
"""

def whoishigher(name='', age='', qage=''):

    if name!='' and age!='' and qage!='':   
        
        if age>qage:
            result = str(name).capitalize() +' es mayor de edad'    	
        else:
            result = str(name).capitalize() +' NO es mayor de edad'
    else:
        result = 'parámetros de entrada no definidos'

    return result

print whoishigher('jennifer', 13, 18)
