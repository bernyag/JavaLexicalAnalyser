#!/usr/bin/env python
# coding: utf-8

# In[21]:


import re as reg

def countByte(expr):
    '''
    Verifica las declaraciones de variables tipo byte del lenguaje Java en su version 8.
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
    patron ="((byte)[ ][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*([0-9][0-9]*|-[0-9][0-9]*){1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*([0-9][0-9]*|-[0-9][0-9]*)){1}|[ ]*))*[ ]*;))|(((byte)[ ]*\[[ ]*\][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*(,[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*)*)}{1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*(,[ ]*([0-9][0-9]*|-[0-9][0-9]*)[ ]*)*}){1}|[ ]*))*[ ]*;))"

    validaPatr = "[0-9][0-9]*|-[0-9][0-9]*"
    
    x = reg.search(patron,expr)
    #Verifico si la línea es válida
    if x:
        #Si es válida, el número de = es el número de instancias
        instancias = reg.findall("([ ]*=[ ]*)",expr)
        
        #Valida si está dentro del rango [-128,127] del tipo byte
        numeros = reg.findall(validaPatr,expr)
        for y in numeros:
            if(not(-128<=int(y)<=127)):
                return (False,-1,-1)

        #El número de , más no es el número de variables declaradas
        declaradas = reg.findall(",[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*",expr)
        if(reg.search("\[ [ ]*\]",expr)):
            arreglo = True
        numInst = len(instancias)
        numDecl = len(declaradas)-len(instancias)+1
    return (arreglo, numDecl, numInst)




