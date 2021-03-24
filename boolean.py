# -*- coding: utf-8 -*-
import re as reg

def countBoolean(expr):
    '''
    Verifica las declaraciones de variables tipo boolean del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de tres parámetros (isArray, nDeclared, nInitialized):
            arreglo (boolean): indica si se declaran arreglos. False si no cumple con la sintaxis.
            numDecl (int): indica el total de variables declaradas. -1 si no cumple con la sintaxis.
            numInst (int): indica el total de variables inicializadas. -1 si no cumple con la sintaxis.
    '''
    arreglo = False
    numDecl = -1
    numInst = -1
    patron ="(((boolean)[ ][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*(true|false)){1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*(true|false)){1}|[ ]*))*[ ]*))|(((boolean)[ ]*\[[ ]*\][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*(true|false)[ ]*(,[ ]*(true|false)[ ]*)*)}{1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*(true|false)[ ]*(,[ ]*(true|false)[ ]*)*}){1}|[ ]*))*[ ]*))"

    x = reg.search(patron,expr)
    #Verifico si la línea es válida
    if x:
        #Si es válida, el número de = es el número de instancias
        instancias = reg.findall("([ ]*=[ ]*)",expr)
        #El número de , más no es el número de variables declaradas
        declaradas = reg.findall("(,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*)",expr)
        contMas = reg.findall("(,[ ]*(false|true))",expr)
        if(reg.search("\[[ ]*\]",expr)):
            arreglo = True
        numInst = len(instancias)
        numDecl = len(declaradas)-len(contMas)+1
    return (arreglo, numDecl, numInst)

