#!/usr/bin/python
# -*- coding: utf-8 -*-
# Jenni - Jenni


"""
1- Crear una funcion que multiplique el valor del primer argumento, sea entero o string por el segundo argumento y lo retorne concatenando con el resultado: 'El resultado de la multiplicacion es...'

"""
def multiplication (a='', b=1):

    if a == '':
	resultado =  'Debe definir al menos un parametro de entrada, entero o string';
    else:
        try:
            result = a * int(b);
            resultado = 'El resultado de la multiplicacion es... '+str(result);
        except ValueError:
            resultado = 'Segundo parametro debe ser entero.';

    return resultado;

    
print multiplication(4, 2);

