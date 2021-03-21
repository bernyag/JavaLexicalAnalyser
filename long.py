import re
import numpy as np

def countLong(expr):
    '''
    Verifica las declaraciones de variables tipo long del lenguaje Java en su version 8.
    Parámetros:
        expression (str): expresión a analizar.
    Regresa: 
        tupla de tres parámetros (array, nDeclared, nInitialized). Si no se cumple con la sintaxis, regresa (False, -1, -1).
            array (boolean): indica si se declaran arreglos.
            nDeclared (int): indica el total de variables declaradas.
            nInitialized (int): indica el total de variables inicializadas.
    '''
    
    # Sintaxis que deben seguir las declaraciones de long[] y long
    pattern = r"^long\s*((\[\s*\]\s*[a-zA-Z_]+\w*((\s*=\s*({(\s*[-+]?((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*)*\s*}|null|new long\s*\[\s*\d+\s*\])(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*)|(\s+[a-zA-Z_]+\w*((\s*=\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))(?!\s*=))?(\s*,\s*[a-zA-Z_]+\w*)?)*))\s*$"
    
    # Verifica la sintaxis
    if re.fullmatch(pattern, expr):
        initialized = re.findall('=', expr) # Encuentra todos los '=' para saber cuántas variables se inicializaron
        
        # Verifica si la declaración es de arreglos
        if re.search("\[[ ]*\]", expr):
            
            # Encuentra todas las ',' para saber cuántas variables se declararon
            # Como tambien pueden existir las ',' dentro de {} (para inicializaciones de arreglos), se eliminan 
            # sin afectar la cadena original y después se realiza la busqueda por las ',' que separan a las variables
            declared = re.split(',', re.sub(r"{\s*[-+]?((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", "{}", expr))
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"{\s*[-+]?((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*))))(\s*,\s*[-+]?((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z])*)))))*\s*}", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    for x in np.array(number.group()[1:-1].split(',')):
                        base = 10
                        if 'b' in x or 'B' in x: base = 2
                        if 'x' in x or 'X' in x: base = 16
                        if not(-2**63 <= int(re.sub(r"\s*|[Ll]|_", '', x), base) <= (2**63)-1): # Verifica que el numero se encuentre dentro del rango para long de Java en su version 8
                            return (False, -1, -1)
                return (True, len(initialized), len(declared))
            else:
                return (True, len(initialized), len(declared))
            
        # Declaraciones que no son de arreglos
        else:
            declared = re.split(',', expr) # Encuentra todas las ',' para saber cuántas variables se declararon
            
            # Arreglo de numeros encontrados en la cadena original (las inicializaciones)
            numbers = re.finditer(r"=\s*[-+]?\s*((\d+(_*\d+)*[Ll])|(0(([bB][01]+(_*[01]+)*)|([xX][0-9A-Za-z]+(_*[0-9A-Za-z]+)*))))", expr)
            if numbers: # Verifica si encontró alguno
                for number in numbers:
                    x = re.sub(r"\s*|[Ll]|_", '', number.group()[1:].strip())
                    base = 10
                    if 'b' in x or 'B' in x: base = 2
                    if 'x' in x or 'X' in x: base = 16
                    if not(-2**63 <= int(x, base) <= (2**63)-1): # Verifica que el numero se encuentre dentro del rango para long de Java en su version 8
                        return (False, -1, -1)
                return (False, len(initialized), len(declared))
            else:
                return (False, len(initialized), len(declared))
    else:
        return (False, -1, -1)
