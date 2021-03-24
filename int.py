# -*- coding: utf-8 -*-
import re as reg
import numpy as np

def countInt(expr):
    '''
    Verifica las declaraciones de variables tipo int del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de tres parámetros (array, nDeclared, nInitialized). Si no se cumple con la sintaxis, regresa (False, -1, -1).
            array (boolean): indica si se declaran arreglos. 
            nDeclared (int): indica el total de variables declaradas.
            nInitialized (int): indica el total de variables inicializadas.
    '''
    
    # Sintaxis que deben seguir las declaraciones de int[] e int
    pattern = r"^int\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*\d+(_*\d+)*(\s*,\s*[-+]?\s*\d+(_*\d+)*)*)*\s*}|null|new int\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*\d+(_*\d+)*(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if reg.fullmatch(pattern, expr): 
        initialized = reg.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Verifica si la declaración es de arreglos
        if reg.search("\[\s*\]", expr):
            
            # Encuentra todas las ',' para saber cuántas variables se declararon
            # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
            # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
            declared = reg.split(',', reg.sub(r"{\s*[-+]?\s*\d+(_*\d+)*(\s*,\s*[-+]?\s*\d+(_*\d+)*)*\s*}", "{}", expr))
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = reg.finditer(r"{\s*[-+]?\s*\d+(_*\d+)*(\s*,\s*[-+]?\s*\d+(_*\d+)*)*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.char.replace(np.char.strip(np.array(number.group()[1:-1].split(','))), ' ', ''):
                        if not(-2**31 <= int(x) <= (2**31)-1): # Verifica que el numero se encuentre dentro del rango para int de Java en su version 8
                            return (False, -1, -1)
                return (True, len(initialized), len(declared))
            else:
                return (True, len(initialized), len(declared))
            
        # Declaraciones que no son de arreglos
        else:
            declared = reg.split(',', expr) # Encuentra todas las ',' para saber cuántas variables se declararon
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = reg.finditer(r"=\s*[-+]?\s*\d+(_*\d+)*", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    if not(-2**31 <= int(number.group()[1:].strip().replace(' ', '')) <= (2**31)-1): # Verifica que el numero se encuentre dentro del rango para int de Java en su version 8
                        return (False, -1, -1)
                return (False, len(initialized), len(declared))
            else:
                return (False, len(initialized), len(declared))
    else:
        return (False, -1, -1)
