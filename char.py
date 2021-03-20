import Lib.re as reg

def countChar(expr):
    '''
    Verifica las declaraciones de variables tipo char del lenguaje Java en su version 8.
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
    patron ="(((char)[ ][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*'.'){1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*'.'){1}|[ ]*))*[ ]*;))|(((char)[ ]*\[[ ]*\][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*'.'[ ]*(,[ ]*'.'[ ]*)*)}{1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*'.'[ ]*(,[ ]*'.'[ ]*)*}){1}|[ ]*))*[ ]*;))"

    x = reg.search(patron,expr)
    #Verifico si la línea es válida
    if x:
        #Si es válida, el número de = es el número de instancias
        instancias = reg.findall("([ ]*=[ ]*)",expr)
        #El número de , más no es el número de variables declaradas
        declaradas = reg.findall(",[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*",expr)
        if(reg.search("\[ [ ]*\]",expr)):
            arreglo = True
        numInst = len(instancias)
        numDecl = len(declaradas)-len(instancias)+1
    return (arreglo, numDecl, numInst)

