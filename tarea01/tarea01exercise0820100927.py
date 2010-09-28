#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
8- Crear una funcion que reciba un rango del 1 al 10 e imprima cuales numeros son impares
"""

def whoispair(rango=xrange(1,10)):

    print 'numeros impares: '
    result=''

    for v in rango:
        if (v%2)==1:
            result = result + str(v) + ', ' 
    return result      


print whoispair(xrange(1, 10))
