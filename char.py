import Lib.re as reg

def checkChar(strCheck):
    arreglo = False
    numDecl = -1
    numInst = -1
    patron ="(((char)[ ][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*'.'){1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*'.'){1}|[ ]*))*[ ]*;))|(((char)[ ]*\[[ ]*\][ ]*([a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*'.'[ ]*(,[ ]*'.'[ ]*)*)}{1}|[ ]*))([ ]*,[ ]*[a-z]([a-zA-Z]|[0-9]|-|_)*(([ ]*=[ ]*{[ ]*'.'[ ]*(,[ ]*'.'[ ]*)*}){1}|[ ]*))*[ ]*;))"

    x = reg.search(patron,strCheck)
    if x:
        instancias = reg.findall("([ ]*=[ ]*)",strCheck)
        declaradas = reg.findall(".,.",strCheck)
        if(reg.search("\[ [ ]*\]",strCheck)):
            arreglo = True
        numInst = len(instancias)
        numDecl = len(declaradas)-len(instancias)+1
    return [arreglo, numDecl, numInst]

