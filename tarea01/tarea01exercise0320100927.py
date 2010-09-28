#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
3- Crear una funcion que reciba numeros creados como strings como argumentos y los reste mostrando el resultado en un entero
"""

def parserint(*p):
    result=0; 

    for v in p:
        
        result = int(v) - result;

    return result;


print parserint('1','2','3','5');



