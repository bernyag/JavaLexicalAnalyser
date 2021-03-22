#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import re as reg

def countShort(expr):
    '''
    Verifica las declaraciones de variables tipo short del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de tres parámetros (isArray, nDeclared, nInitialized):
            arreglo (boolean): indica si se declaran arreglos. False si no cumple con la sintaxis.
            numDecl (int): indica el total de variables declaradas. -1 si no cumple con la sintaxis.
            n (int): indica el total de variables inicializadas. -1 si no cumple con la sintaxis.
    '''
    arreglo = False
    numDecl = -1
    numInst = -1
    patron ="((short)[ ][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*([0-9][0-9]*|-[0-9][0-9]*){1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*([0-9][0-9]*|-[0-9][0-9]*)){1}|[ ]*))*[ ]*))|(((short)[ ]*\[[ ]*\][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*(,[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*)*)}{1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*(,[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*)*}){1}|[ ]*))*[ ]*))"

    validaPatr = "[0-9][0-9]*|-[0-9][0-9]*"
    
    x = reg.search(patron,expr)
    #Verifico si la línea es válida
    if x:
        #Si es válida, el número de = es el número de instancias
        instancias = reg.findall("([ ]*=[ ]*)",expr)
        
        #Valida si está dentro del rango [-32768,32767] del tipo short
        numeros = reg.findall(validaPatr,expr)
        for y in numeros:
            if(not(-32768<=int(y)<=32767)):
                return (False,-1,-1)

        #El número de , más no es el número de variables declaradas
        declaradas = reg.findall(",[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*",expr)
        if(reg.search("\[[ ]*\]",expr)):
            arreglo = True
        numInst = len(instancias)
        numDecl = len(declaradas)-len(instancias)+1
    return (arreglo, numDecl, numInst)




