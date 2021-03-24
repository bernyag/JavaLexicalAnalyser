# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 19:59:38 2021

@author: Ivana
"""
# Se importa la librería y los archivos que se usaran para evaluar las expresiones

import sys
# sys.path is a list of absolute path strings
sys.path.insert(1,'\\Documents\\FMC\\JavaLexicalAnalyser')
import re
from short import countShort
from Long import countLong
from Int import countInt
from boolean import countBoolean
from byte import countByte
from char import countChar
from doubleFloat import countFloat, countDouble
from String import countString
from regex import info

# Se leen las expresiones de un archivo de texto
file = open("java-regex.txt", "r")
content = file.read()
lines = content.split(';')
file.close()

print("Expresiones a evaluar \n")
print(lines, "\n")

# El método split deja como último elemento de la lista un espacio por lo que 
# se elimina con el método pop()
lines.pop()
# Con el método lstrip se elimina el espacio en blanco con el que inicia cada expresión que dejo el método slpit().
# Así la primera palabra en cada expresion debe indicar el tipo de dato
lines = [x.lstrip() for x in lines]

# Se inicializan los contadores en 0
counters = {
    "int": (0,0),
    "int[]": (0,0),
    "String": (0,0),
    "String[]": (0,0),
    "boolean": (0,0),
    "boolean[]": (0,0),
    "char": (0,0),
    "char[]": (0,0),
    "byte": (0,0),
    "byte[]": (0,0),
    "short": (0,0),
    "short[]": (0,0),
    "long": (0,0),
    "long[]": (0,0),
    "float": (0,0),
    "float[]": (0,0),
    "double": (0,0),
    "double[]": (0,0)
}

type_var = {
    "int": set(),
   "int[]": set(),
    "String": set(),
    "String[]": set(),
    "boolean": set(),
    "boolean[]": set(),
    "char": set(),
    "char[]": set(),
    "byte": set(),
    "byte[]": set(),
    "short": set(),
    "short[]": set(),
    "long": set(),
    "long[]": set(),
    "float": set(),
    "float[]": set(),
    "double": set(),
    "double[]": set()}

# la siguiente función manda a evaluar la expresión en cada línea de acuerdo a su tipo
def switch(label, line):
    switcher={
        "int": (lambda x: countInt(x))(line),
        "int[]": (lambda x: countInt(x))(line),
        "String": (lambda x: countString(x))(line),
        "String[]": (lambda x: countString(x))(line),
        "boolean": (lambda x: countBoolean(x))(line),
        "boolean[]": (lambda x: countBoolean(x))(line),
        "char": (lambda x: countChar(x))(line),
        "char[]": (lambda x: countChar(x))(line),
        "byte": (lambda x: countByte(x))(line),
        "byte[]": (lambda x: countByte(x))(line),
        "short": (lambda x: countShort(x))(line),
        "short[]": (lambda x: countShort(x))(line),
        "long": (lambda x: countLong(x))(line),
        "long[]": (lambda x: countLong(x))(line),
        "float": (lambda x: countFloat(x))(line),
        "float[]": (lambda x: countFloat(x))(line),
        "double": (lambda x: countDouble(x))(line),
        "double[]": (lambda x: countDouble(x))(line),
        }
    return switcher.get(label,(100, 100))

for line in lines:
    valid = switch(line.split()[0], line)[1:] != (-1,-1)
    if valid:
        print("La expresión: ", line, " es una declaración válida de la variable ", line.split()[0] , " en Java 8 \n")
        counters[ line.split()[0] ] = tuple(map(sum,zip(counters[ line.split()[0] ], switch( line.split()[0], line)[1:])),)
    else: 
        print("La expresión: ", line, " no es una declaración válida de la variable ", line.split()[0] , " en Java 8 \n" )

totDeclaradas = 0;
totInicializadas = 0;
totArrDec = 0;
totArrIni = 0;
tipoVar = counters.keys()
for x in tipoVar:
    totDeclaradas += counters[x][0];
    totInicializadas += counters[x][1];
    if x[-2:] == "[]":
        totArrDec += counters[x][0];
        totArrIni += counters[x][1];
print("------------------  Resultados  ----------------- \n")      
print("Total de variables declaradas: " + str(totDeclaradas) + "\n") 
print("Total de variables inicializadas: " + str(totInicializadas) + "\n") 
print("Total de variables tipo arreglo declaradas: " + str(totArrDec) + "\n") 
print("Total de variables tipo arreglo inicializadas: " + str(totArrIni) + "\n") 
print("Clasificación de los nombres de las variables de acuerdo a su tipo:  \n")
for line in lines:
    name = info(line)[-1]
    for x in name:
        type_var[line.split()[0]].add(x)
type_var