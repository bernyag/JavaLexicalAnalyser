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


def countByte(expr):
    '''
    Verifica las declaraciones de variables tipo byte del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cuatro parámetros (array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (False, -1, -1, []).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    
    # Sintaxis que deben seguir las declaraciones de byte[] y byte
    pattern = r"^byte\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*)*\s*}|null|new byte\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        base = 10
                        if 'b' in x or 'B' in x: base = 2
                        if 'x' in x or 'X' in x: base = 16
                        if not(-128 <= int(re.sub(r"\s*|_", '', x), base) <= 127): # Verifica que el numero se encuentre dentro del rango para byte de Java en su version 8
                            return (False, -1, -1, [])
                return (True, len(initialized), len(declared), varNames(declared))
            else:
                return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = re.sub(r"\s*|_", '', number.group()[1:].strip())
                    base = 10
                    if 'b' in x or 'B' in x: base = 2
                    if 'x' in x or 'X' in x: base = 16
                    if not(-128 <= int(x, base) <= 127): # Verifica que el numero se encuentre dentro del rango para byte de Java en su version 8
                        return (False, -1, -1, [])
                return (False, len(initialized), len(declared), varNames(declared))
            else:
                return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
    

def countShort(expr):
    '''
    Verifica las declaraciones de variables tipo short del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cuatro parámetros (array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (False, -1, -1, []).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    
    # Sintaxis que deben seguir las declaraciones de short[] y short
    pattern = r"^short\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*)*\s*}|null|new short\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        base = 10
                        if 'b' in x or 'B' in x: base = 2
                        if 'x' in x or 'X' in x: base = 16
                        if not(-32768 <= int(re.sub(r"\s*|_", '', x), base) <= 32767): # Verifica que el numero se encuentre dentro del rango para short de Java en su version 8
                            return (False, -1, -1, [])
                return (True, len(initialized), len(declared), varNames(declared))
            else:
                return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = re.sub(r"\s*|_", '', number.group()[1:].strip())
                    base = 10
                    if 'b' in x or 'B' in x: base = 2
                    if 'x' in x or 'X' in x: base = 16
                    if not(-32768 <= int(x, base) <= 32767): # Verifica que el numero se encuentre dentro del rango para short de Java en su version 8
                        return (False, -1, -1, [])
                return (False, len(initialized), len(declared), varNames(declared))
            else:
                return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
    
    
def countInt(expr):
    '''
    Verifica las declaraciones de variables tipo int del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cuatro parámetros (array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (False, -1, -1, []).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    
    # Sintaxis que deben seguir las declaraciones de int[] y int
    pattern = r"^int\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*)*\s*}|null|new int\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        base = 10
                        if 'b' in x or 'B' in x: base = 2
                        if 'x' in x or 'X' in x: base = 16
                        if not(-2**31 <= int(re.sub(r"\s*|_", '', x), base) <= (2**31)-1): # Verifica que el numero se encuentre dentro del rango para int de Java en su version 8
                            return (False, -1, -1, [])
                return (True, len(initialized), len(declared), varNames(declared))
            else:
                return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*((\d+(_*\d+)*)|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = re.sub(r"\s*|_", '', number.group()[1:].strip())
                    base = 10
                    if 'b' in x or 'B' in x: base = 2
                    if 'x' in x or 'X' in x: base = 16
                    if not(-2**31 <= int(x, base) <= (2**31)-1): # Verifica que el numero se encuentre dentro del rango para int de Java en su version 8
                        return (False, -1, -1, [])
                return (False, len(initialized), len(declared), varNames(declared))
            else:
                return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
    
    
def countLong(expr):
    '''
    Verifica las declaraciones de variables tipo long del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de tres parámetros (array, nDeclared, nInitialized). Si no se cumple con la sintaxis, regresa (False, -1, -1).
            array (boolean): indica si se declaran arreglos.
            nDeclared (int): indica el total de variables declaradas.
            nInitialized (int): indica el total de variables inicializadas.
    '''
    
    # Sintaxis que deben seguir las declaraciones de long[] y long
    pattern = r"^long\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*)*\s*}|null|new long\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        base = 10
                        if 'b' in x or 'B' in x: base = 2
                        if 'x' in x or 'X' in x: base = 16
                        if not(-2**63 <= int(re.sub(r"\s*|[Ll]|_", '', x), base) <= (2**63)-1): # Verifica que el numero se encuentre dentro del rango para long de Java en su version 8
                            return (False, -1, -1, [])
                return (True, len(initialized), len(declared), varNames(declared))
            else:
                return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = re.sub(r"\s*|[Ll]|_", '', number.group()[1:].strip())
                    base = 10
                    if 'b' in x or 'B' in x: base = 2
                    if 'x' in x or 'X' in x: base = 16
                    if not(-2**63 <= int(x, base) <= (2**63)-1): # Verifica que el numero se encuentre dentro del rango para long de Java en su version 8
                        return (False, -1, -1, [])
                return (False, len(initialized), len(declared), varNames(declared))
            else:
                return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
    
    
def countFloat(expr):
    '''
    Verifica las declaraciones de variables tipo float del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cuatro parámetros (array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (False, -1, -1, []).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    
    # Sintaxis que deben seguir las declaraciones de float[] y float
    pattern = r"^float\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF](\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF])*)*\s*}|null|new float\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF](?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr): 
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF](\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF])*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[\s*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF](\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF])*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        x = float(re.sub(r"\s*|[fF]|_", '', x))
                        if x > 0:
                            if not(1.40239846e-45 <= x <= 3.40282347e+38): # Verifica que el numero se encuentre dentro del rango positivo para float de Java en su version 8
                                return (False, -1, -1, [])
                        if x < 0:
                            if not(-3.40282347e+38 <= x <= -1.40239846e-45): # Verifica que el numero se encuentre dentro del rango negativo para float de Java en su version 8
                                return (False, -1, -1, [])
                return (True, len(initialized), len(declared), varNames(declared))
            else:
                return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[fF]", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = float(re.sub(r"\s*|[fF]|_", '', number.group()[1:].strip()))
                    if x > 0:
                        if not(1.40239846e-45 <= x <= 3.40282347e+38): # Verifica que el numero se encuentre dentro del rango positivo para float de Java en su version 8
                            return (False, -1, -1, [])
                    if x < 0:
                        if not(-3.40282347e+38 <= x <= -1.40239846e-45): # Verifica que el numero se encuentre dentro del rango negativo para float de Java en su version 8
                            return (False, -1, -1, [])
                return (False, len(initialized), len(declared), varNames(declared))
            else:
                return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
    
    
def countDouble(expr):
    '''
    Verifica las declaraciones de variables tipo double del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cuatro parámetros (array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (False, -1, -1, []).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    
    # Sintaxis que deben seguir las declaraciones de double[] y double
    pattern = r"^double\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?(\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?)*)*\s*}|null|new double\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr): 
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?(\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?)*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[\s*\]", expr):
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?(\s*,\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?)*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        x = float(re.sub(r"\s*|[dD]|_", '', x))
                        if x > 0:
                            if not(4.9406564584124654e-324 <= x <= 1.7976931348623157e+308): # Verifica que el numero se encuentre dentro del rango para double de Java en su version 8
                                return (False, -1, -1, [])
                        elif x < 0:
                            if not(-1.7976931348623157e+308 <= x <= -4.9406564584124654e-324): # Verifica que el numero se encuentre dentro del rango para double de Java en su version 8
                                return (False, -1, -1, [])
                return (True, len(initialized), len(declared), varNames(declared))
            else:
                return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*\d+(_*\d+)*(\.\d+)?(_*\d+)*(e\d+)?[dD]?", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = float(re.sub(r"\s*|[dD]|_", '', number.group()[1:].strip()))
                    if x > 0:
                        if not(4.9406564584124654e-324 <= x <= 1.7976931348623157e+308): # Verifica que el numero se encuentre dentro del rango para double de Java en su version 8
                            return (False, -1, -1, [])
                    elif x < 0:
                        if not(-1.7976931348623157e+308 <= x <= -4.9406564584124654e-324): # Verifica que el numero se encuentre dentro del rango para double de Java en su version 8
                            return (False, -1, -1, [])
                return (False, len(initialized), len(declared), varNames(declared))
            else:
                return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
    
    
def countChar(expr):
    '''
    Verifica las declaraciones de variables tipo char del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cuatro parámetros (array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (False, -1, -1, []).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    # Sintaxis que deben seguir las declaraciones
    pattern = r"^char\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*'.'\s*(\s*,\s*'.')*)*\s*}|null|new char\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*'.'(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{(\s*'.'\s*(\s*,\s*'.')*)*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
    
    
def countString(expr):
    '''
    Verifica las declaraciones de variables tipo String del lenguaje Java en su version 8.
    Parámetros:
        expr (str): expresión a analizar.
    Regresa: 
        tupla de cuatro parámetros (array, len(initialized), len(declared), varNames(declared)). Si no se cumple con la sintaxis, regresa (False, -1, -1, []).
            array (boolean): indica si se declaran arreglos.
            len(initialized) (int): indica el total de variables inicializadas.
            len(declared) (int): indica el total de variables declaradas.
            varNames(declared) (list): indica los nombres de las variables.
    '''
    # Sintaxis que deben seguir las declaraciones
    pattern = r"^String\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*\".*\"\s*(\s*,\s*\".*\")*)*\s*}|null|new String\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*\".*\"(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Encuentra todas las ',' para saber cuántas variables se declararon
        # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan
        # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
        declared = re.split(',', re.sub(r"{(\s*\".*\"\s*(\s*,\s*\".*\")*)*\s*}", "{}", expr))
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            return (True, len(initialized), len(declared), varNames(declared))
            
        # Declaraciones que no son de arreglos
        else:
            return (False, len(initialized), len(declared), varNames(declared))
    else:
        return (False, -1, -1, [])
