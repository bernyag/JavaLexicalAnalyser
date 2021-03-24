# -*- coding: utf-8 -*-
import re
import numpy as np

def varNames(declared):
    '''
    Encuentra los nombres de variables.
    Parámetros:
        declared (list): expresión de entrada separada por ','.
    Regresa:
        variables (list): nombres de variables ordenados alfabéticamente.
    '''
    variables = [x.strip() for x in declared]
    variables = [re.sub(r"\s*=\s*.+", '', var) for var in variables]
    variables[0] = re.sub(r"^\w+\s*(\[\s*\])?\s*", '', variables[0], 1)
    return sorted(variables)


def isInteger(var, expr):
    '''
    Verifica las declaraciones de variables tipo byte, short, int y long del lenguaje Java en su version 8.
    Parámetros:
        var (str): tipo de variable(s) de la expresión.
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cinco parámetros (var, array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (None, False, -1, -1, []).
            var (str): indica el tipo de variable(s) declarada(s).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    end = "" # Para long, los enteros deben terminar en "L" o "l"
    limInf = 0 # limite inferior del rango que acepta Java 8 para la variable primitiva
    limSup = 0 # limite superior del rango que acepta Java 8 para la variable primitiva
    
    if var == "byte":
        limInf = -128
        limSup = 127
    elif var == "short":
        limInf = -32768
        limSup = 32767
    elif var == "int":
        limInf = -2**31
        limSup = (2**31)-1
    elif var == "long":
        end = "[Ll]"
        limInf = -2**63
        limSup = (2**63)-1
        
    # Sintaxis que deben seguir las declaraciones
    pattern = r"^"+var+"\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*((\d+(_*\d+)*"+end+")|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*"+end+")|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*)*\s*}|null|new "+var+"\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*((\d+(_*\d+)*"+end+")|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*((\d+(_*\d+)*[Ll]?)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*[Ll]?)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", "{}", expr))
        
        # Verifica que los nombres de las variables aparezcan una sola vez en la expresión
        if len(set(varNames(declared))) != len(declared):
            return (None, False, -1, -1, [])
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*((\d+(_*\d+)*[Ll]?)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*[Ll]?)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        base = 10
                        if 'b' in x or 'B' in x: base = 2
                        if 'x' in x or 'X' in x: base = 16
                        if not(limInf <= int(re.sub(r"\s*|[Ll]|_", '', x), base) <= limSup): # Verifica que el numero se encuentre dentro del rango para el tipo de variable primitiva de Java en su version 8
                            return (None, False, -1, -1, [])
                return (var, True, len(initialized), len(declared), varNames(declared))
            else:
                return (var, True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*((\d+(_*\d+)*[Ll]?)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = re.sub(r"\s*|[Ll]|_", '', number.group()[1:].strip())
                    base = 10
                    if 'b' in x or 'B' in x: base = 2
                    if 'x' in x or 'X' in x: base = 16
                    if not(limInf <= int(x, base) <= limSup): # Verifica que el numero se encuentre dentro del rango para el tipo de variable primitiva de Java en su version 8
                        return (None, False, -1, -1, [])
                return (var, False, len(initialized), len(declared), varNames(declared))
            else:
                return (var, False, len(initialized), len(declared), varNames(declared))
    else:
        return (None, False, -1, -1, [])


def isFloatingPoint(var, expr):
    '''
    Verifica las declaraciones de variables tipo float y double del lenguaje Java en su version 8.
    Parámetros:
        var (str): tipo de variable(s) de la expresión.
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cinco parámetros (var, array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (None, False, -1, -1, []).
            var (str): indica el tipo de variable(s) declarada(s).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    end = "" # Para float, los numeros deben terminar en "f" o "f"
    limInf = 0 # limite inferior del rango que acepta Java 8 para la variable primitiva
    limSup = 0 # limite superior del rango que acepta Java 8 para la variable primitiva
    
    if var == "float":
        end = "[fF]"
        limInf = 1.40239846e-45
        limSup = 3.40282347e+38
    elif var == "double":
        end = "[dD]?"
        limInf = 4.9406564584124654e-324
        limSup = 1.7976931348623157e+308
    
    # Sintaxis que deben seguir las declaraciones
    pattern = r"^"+var+"\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?"+end+"(\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?"+end+")*)*\s*}|null|new "+var+"\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?"+end+"(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr): 
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fFdD]?(\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fFdD]?)*\s*}", "{}", expr))
        
        # Verifica que los nombres de las variables aparezcan una sola vez en la expresión
        if len(set(varNames(declared))) != len(declared):
            return (None, False, -1, -1, [])
        
        # Verifica si la declaración es de arreglos
        if re.search("\[\s*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fFdD]?(\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fFdD]?)*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        x = float(re.sub(r"\s*|[fFdD]|_", '', x))
                        if x < 0:
                            if not(-limSup <= x <= -limInf): # Verifica que el numero se encuentre dentro del rango negativo para el tipo de variable primitiva de Java en su version 8
                                return (None, False, -1, -1, [])
                        elif x > 0:
                            if not(limInf <= x <= limSup): # Verifica que el numero se encuentre dentro del rango positivo para el tipo de variable primitiva de Java en su version 8
                                return (None, False, -1, -1, [])
                return (var, True, len(initialized), len(declared), varNames(declared))
            else:
                return (var, True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fFdD]?", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = float(re.sub(r"\s*|[fFdD]|_", '', number.group()[1:].strip())) 
                    if x < 0:
                        if not(-limSup <= x <= -limInf): # Verifica que el numero se encuentre dentro del rango negativo para el tipo de variable primitiva de Java en su version 8
                            return (None, False, -1, -1, [])
                    elif x > 0:
                        if not(limInf <= x <= limSup): # Verifica que el numero se encuentre dentro del rango positivo para el tipo de variable primitiva de Java en su version 8
                            return (None, False, -1, -1, [])
                return (var, False, len(initialized), len(declared), varNames(declared))
            else:
                return (var, False, len(initialized), len(declared), varNames(declared))
    else:
        return (None, False, -1, -1, [])
    
    
def isNotNumber(var, expr):
    '''
    Verifica las declaraciones de variables tipo char, String y boolean del lenguaje Java en su version 8.
    Parámetros:
        var (str): tipo de variable(s) de la expresión.
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cinco parámetros (var, array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (None, False, -1, -1, []).
            var (str): indica el tipo de variable(s) declarada(s).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    values = "" # fomato que aceptan las variables
    
    if var == "char":
        values = "'.'"
    elif var == "String":
        values = "\".*\""
    elif var == "boolean":
        values = "(true|false)"
    
    # Sintaxis que deben seguir las declaraciones
    pattern = r"^"+var+"\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*"+values+"\s*(\s*,\s*"+values+")*)*\s*}|null|new "+var+"\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*"+values+"(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{(\s*"+values+"\s*(\s*,\s*"+values+")*)*\s*}", "{}", expr))
        
        # Verifica que los nombres de las variables aparezcan una sola vez en la expresión
        if len(set(varNames(declared))) != len(declared):
            return (None, False, -1, -1, [])
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            return (var, True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            return (var, False, len(initialized), len(declared), varNames(declared))
    else:
        return (None, False, -1, -1, [])
    
    
def info(expr):
    '''
    Verifica las declaraciones de variables primitivas y String del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cinco parámetros (var, array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (None, False, -1, -1, []).
            var (str): indica el tipo de variable(s) declarada(s).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    if re.search(r"^byte", expr):
        return isInteger("byte", expr)
    
    elif re.search(r"^short", expr):
        return isInteger("short", expr)
    
    elif re.search(r"^int", expr):
        return isInteger("int", expr)
    
    elif re.search(r"^long", expr):
        return isInteger("long", expr)
    
    elif re.search(r"^float", expr):
        return isFloatingPoint("float", expr)
    
    elif re.search(r"^double", expr):
        return isFloatingPoint("double", expr)
    
    elif re.search(r"^char", expr):
        return isNotNumber("char", expr)
    
    elif re.search(r"^String", expr):
        return isNotNumber("String", expr)
    
    elif re.search(r"^boolean", expr):
        return isNotNumber("boolean", expr)
    
    else:
        return (None, False, -1, -1, [])
