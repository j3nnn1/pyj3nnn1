#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
2- Crear una funcion que reciba parametros sin determinar y que nos regrese lo siguiente como llave/valor: Nombre = Su_Nombre, Apellido = Su_Apellido, Ciudad = Su_Ciudad y ademas, al menos tres valores opcionales

"""

def getpersonaldata (*param):
    
    if len(param)>=3:

       datahash={'Nombre':param[0],'Apellido':param[1], 'Ciudad':param[2]};

       for l,v in (enumerate(param[3:])):
            datahash.update({'Opc. '+(str(l + 1)):v});

    else:
       datahash='Debe indicar los primeros 3 parametros.';    

    return datahash;

print getpersonaldata('Jennifer', 'Maldonado', 'Opcional', 'Pcipnal2','Who');

