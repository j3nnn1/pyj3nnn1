#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
6- Crear una funcion que reciba los argumentos de Nombre y edad y te diga si esa persona, de manera concatenada, sea mayor o no
"""

def whoishigher(name='', age=''):

    if name!='' and age!='':   

        if age>18:
            result = str(name)+' es mayor de edad'    	
        else:
            result = str(name)+' NO es mayor de edad'
    else:
        result = 'parámetros de entrada no definidos'

    return result

print whoishigher('jennifer', 21)
