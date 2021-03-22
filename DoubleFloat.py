import re as re
'''
    Double
    Verifica las declaraciones double del lenguaje Java en su version 8.
    Parámetros:
        test (str): cadena que se debe analizar.
    Regresa: 
        tupla (esArreglo, totIni+totDec, totDec):
            esArreglo (boolean): indica si se declaran arreglos. 
            totIni+totDec (int): indica el total de variables declaradas. 
            totDec (int): indica el total de variables inicializadas.
    '''

def countDouble(test):
    esArreglo=False
    totIni=0
    totDec=0
    tst=test.replace(" ", "")
    try:
        if(tst.count('double')==1):
            tst=tst.replace("double", "")
            tst=tst.replace(";", "")
            if(tst[:2]=='[]' or tst[-2:]=='[]'):
                esArreglo=True
                tst=tst.replace("[]", "")
            [totIni,nombre]=CuentaIni(tst)
            [totDec,nombre2]=CuentaDec(tst)
        else:
            raise Exception()
    except:
        #print("Declaración incorrecta: "+test)
        esArreglo=False
        totIni=0
        totDec=-1
        nombre=""
    return [esArreglo, totIni+totDec, totDec]  

def countFloat(test):
    esArreglo=False
    totIni=0
    totDec=0
    tst=test.replace(" ", "")
    try:
        if(tst.count('float')==1):
            tst=tst.replace("float", "")
            tst=tst.replace(";", "")
            if(tst[:2]=='[]' or tst[-2:]=='[]'):
                esArreglo=True
                tst=tst.replace("[]", "")
            [totIni,nombre]=CuentaIni(tst)
            [totDec,nombre2]=CuentaDecFloat(tst)
        else:
            raise Exception()
    except:
        #print("Declaración incorrecta: "+test)
        esArreglo=False
        totIni=0
        totDec=-1
        nombre=""
    return [esArreglo, totIni+totDec, totDec]  

def CuentaIni(test):
    lst=test.split(",")
    p = re.compile("^[A-Za-z0-9]*$")
    l2 = [ s for s in lst if p.match(s)]
    if ("" in l2):
        raise Exception()
    return [len(l2),l2]

def CuentaDec(test):
    lst=test.split(",")
    p = [re.findall(r'(.*)=', x) for x in lst]
    p= [item for sublist in p for item in sublist]
    l2 = [re.findall(r'=(.*)', x) for x in lst]
    l2= [item for sublist in l2 for item in sublist]
    for x in l2:
        if (abs(float(x))<4.9e-34 or abs(float(x))>1.8e+308): 
            raise Exception()
    return [len(l2),p]

def CuentaDecFloat(test):
    lst=test.split(",")
    p = [re.findall(r'(.*)=', x) for x in lst]
    p= [item for sublist in p for item in sublist]
    l2 = [re.findall(r'=(.*)', x) for x in lst]
    l2= [item for sublist in l2 for item in sublist]
    for x in l2:
        if(x[-1]=="f" or x[-1]=="F"):
            x=x[:-1]
            float(x)
        else:
            raise Exception()
    return [len(l2),p]