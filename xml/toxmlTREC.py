#!/usr/bin/python
# -*- coding: utf-8 -*-
#.I identificador del documento
#
#DOC
# DOCNO
# S
# M
# T
# P
# W
# A
#/DOC
from xml.dom import minidom # for a pretty xml
#import xml.etree.ElementTree as xml
from lxml import etree as xml # it's better than only ET
import os
import re #testing re

try:
    file = open('corpus_evaluar/ohsumed.87', 'r');
except IOError:
    print('Hola que hace?, File not exist!')
except:
    print('Ups.. Unexpected Error!')

pattern = re.compile(r'(\d+)')

root = xml.Element('terrier')
#this is bad, I know. :(  Python FILE on memory RAM. I don't know other way
lines = file.readlines()
size = len(lines)

for count, line  in enumerate(lines):
    nextline = count + 1 
    #if (re.match('\.I', line)): # much procesador not good
    if (line[0:2].strip()=='.I'):
        #id = pattern.search(line).group(0) 
        child = xml.Element('DOC')      ##create child
        root.append(child)              ##add 

    if(line.strip()=='.U'):
        if (nextline < size):
            docno = lines[nextline].strip()
            child2 = xml.Element('DOCNO')   ##setting attr DOCNO
            child2.text = docno
            child.append(child2)
    if (line.strip()=='.S'):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('S')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)
    if (line.strip()=='.M'):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('M')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)
    if (line.strip()=='.T'):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('T')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)
 
    if (line.strip()=='.P'):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('P')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)

    if (line.strip()=='.W'):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('W')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)

    if (line.strip()=='.A'):
        if (nextline < size):
            source = lines[nextline].strip()
            child2 = xml.Element('A')   ##setting attr DOCNO
            child2.text = source
            child.append(child2)

xml.ElementTree(root).write('ohsumed87.xml', pretty_print=True)
file.close()

