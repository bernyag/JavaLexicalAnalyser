#!/usr/bin/env python
# coding: utf-8

# In[19]:


import re

def sintaxAnalyzer(tokens):
    valido = True
    n=len(tokens)
    print(n)
    i=0
    while (i < n and valido):
        if (tokens[i] == 'while'):
            if(i + 5< n): 
                cad = str(tokens[i+1]) + str(tokens[i+2])+str(tokens[i+3])+str(tokens[i+4])+str(tokens[i+5])
                print(cad)
                valido = revisaExpresion(cad)
                i=i+5
                if ( i + 1 <n and ~valido):
                    cad = cad + str(tokens[i])
                    valido = revisaExpresion(cad)
            else:
                valido = False
        else:                
            i=i+1    
    return valido


def revisaExpresion(cad):
    res = re.search("\(([a-zA-Z]|[0-9])(<|>|<=|>=|==|!=)([a-zA-Z]|[0-9])\)",cad)
    return res != None

def test():
    p1 = ['while', '(' , 'a', '==', 'b',')','{','while','(','7','<','8',')','}']
    p2 = ['while', '(' , 'a', '==', 'b',')','{','while','(','while','<','8',')','}']
    p3 = ['while', '(' , 'a', '==', 'b',')','{','while','(','7','while','8',')','}']
    p4 = ['while', '(' , 'a', '==', 'b',')','{','while','(','7','<','8','9','}']
    p5 = ['while', '(' , 'a', '==', 'b',')','{','while','7','7','<','8',')','}','a']
    
    p6  = ['while', '[' , 's', '<=', 'xx',']','{','while','(','5','<','2',')','}']
    p7  = ['while', '(' , '4', '=>', 'y',')','{','while','(','g','while','y',')','}']
    p8  = ['while', '(' , 'a', '<', 'b',')','{','while','7','7','<','8',')','}','a']
    p9  = ['while', '(' , 'a', '>', 'b',')','{','while','1','<','q',')','}','a>2']
    p10 = ['while', '(' , 'y', '>=', 'y',')','{','while','(','g','while','y',')','}']
    
    p11 = ['while', '(' , 'a', '==', 'b',')','{','while','(','6','<','r',')','}']
    p12 =['while', '(' , 's', '<=', 'd',')','{','while','(','7','<','8',')','{','while','(','7','==','8',')','{','}','}','}']
    p13 = ['while', '(' , 'z', '=>', '1',')','{','while','(','4','<','t',')','{','while','(','y','==','8',')','{','while','(','7','==','8',')','{','}','}','}','}']
    p14 = ['while', '(' , '3', '>=', '6',')','{','while','(','7','<','x',')','{','while','(','7','==','8',')','{','while','(','u','==','8',')','{','while','(','y','==','8',')','{','}','}','}','}','}']
    p15 =['while', '(' , 'q', '==', 'g',')','{','while','(','1','<','5',')','{','while','(','h','==','2',')','{','while','(','7','==','8',')','{','while','(','t','==','2',')','{','while','(','i','==','y',')','{','}','}','}','}','}','}']
    
    print('p1')
    print(sintaxAnalyzer(p1))
    print('p2')
    print(sintaxAnalyzer(p2))
    print('p3')
    print(sintaxAnalyzer(p3))
    print('p4')
    print(sintaxAnalyzer(p4))
    print('p5')
    print(sintaxAnalyzer(p5))
    
    print('p6')
    print(sintaxAnalyzer(p6))
    print('p7')
    print(sintaxAnalyzer(p7))
    print('p8')
    print(sintaxAnalyzer(p8))
    print('p9')
    print(sintaxAnalyzer(p9))
    print('p10')
    print(sintaxAnalyzer(p10))
    
    print('p11')
    print(sintaxAnalyzer(p11))
    print('p12')
    print(sintaxAnalyzer(p12))
    print('p13')
    print(sintaxAnalyzer(p13))
    print('p14')
    print(sintaxAnalyzer(p14))
    print('p15')
    print(sintaxAnalyzer(p15))


# In[20]:


test()


# In[ ]:





# In[ ]:




