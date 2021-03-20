import re

def countInt(expr):
    '''
    Verifica las declaraciones de variables tipo int del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de tres parámetros (isArray, nDeclared, nInitialized):
            isArray (boolean): indica si se declaran arreglos. False si no cumple con la sintaxis.
            nDeclared (int): indica el total de variables declaradas. -1 si no cumple con la sintaxis.
            nInitialized (int): indica el total de variables inicializadas. -1 si no cumple con la sintaxis.
    '''
    numInArray = "{[ ]*(\+|-)*\d*[ ]*(,[ ]*(\+|-)*\d+[ ]*)*}"
    pattern = "(int[ ]+([a-z_A-Z]+\w*((([ ]*=[ ]*(\+|-)*\d+){0,1})(?!([ ]*=[ ]*)|([a-z_A-Z]))([ ]*,[ ]*[a-z_A-Z]+\w*)*)*)+[ ]*)|(int[ ]*\[[ ]*\][ ]*([a-z_A-Z]+\w*((([ ]*=[ ]*(null|(new[ ]*int[ ]*\[[ ]*\d+[ ]*\])|("+numInArray+"))){0,1})(?!([ ]*=[ ]*)|([a-z_A-Z]))([ ]*,[ ]*[a-z_A-Z]+\w*)*)*)+[ ]*)"
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr)
        if re.search("\[[ ]*\]", expr):
            declared = re.split(',', re.sub(numInArray, "{}", expr))
            return (True, len(initialized), len(declared))
        else:
            declared = re.split(',', expr)
            return (False, len(initialized), len(declared)) 
    else:
        return (False, -1, -1)