#!/usr/bin/python
# -*- coding: utf-8 -*-
# j3nnn1 - 0.0.0 -
#.I identificador del documento
#
#DOC
# DOCNO
#
from xml.dom import minidom
#import xml.etree.ElementTree as ET
#import xml.etree.ElementTree as xml
from lxml import etree as xml
import os
import re

try:
    file = open('corpus_evaluar/ohsumed.87', 'r');
except IOError:
    print('Hola que hace?, File not exist!')
except:
    print('Ups.. Error inesperado!')


#x = ('xxx', 'abcxxxabc', 'xyx', 'abc', 'x.x', 'axa', 'axxxxa', 'axxya')

#dir(filter((lambda s: re.match(r'xxx', s)), x))

pattern = re.compile(r'(\d+)')


root = xml.Element('terrier')
#this is bad, I know. :(  Python FILE on memory RAM. I don't know other way
lines = file.readlines()
size = len(lines)

for count, line  in enumerate(lines):
    nextline = count + 1 
    if (re.match('\.I', line)):
        id = pattern.search(line).group(0)
        child = xml.Element('DOC')      ##create child
        root.append(child)              ##add 

    if(re.match('\.U', line)):
    
        if (nextline < size):
            docno = lines[nextline].strip()
            child2 = xml.Element('DOCNO')   ##setting attr DOCNO
            child2.text = docno
            child.append(child2)
    if (re.match('\.S',line)):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('S')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)
    if (re.match('\.M',line)):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('M')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)
    if (re.match('\.T',line)):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('T')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)
 
    if (re.match('\.P',line)):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('P')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)

    if (re.match('\.W',line)):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('W')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)

    if (re.match('\.A',line)):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('A')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)

xml.ElementTree(root).write('testing.xml', pretty_print=True)
file.close()

