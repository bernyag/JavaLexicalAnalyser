from char import *
from String import *
from boolean import *
print(countChar("char a='c', b, c ;"))
print(countChar("char a='c', b, ;"))
print(countChar("char[] chArr = {'A', 'B', 'C'}, b, c ;"))
print(countString("String a=\"c\", b, c ;"))
print(countString("String a=\"c\", b, ;"))
print(countString("String[ ] a={\"asdc\" , \"55qew6as\"}, b, c ;"))
print(countBool(" boolean [ ] blArr = {true, false, true};"))
print(countBool("boolean [ ] a = {true,false,true}, b ={true,  false};"))
print(countBool("boolean a = True;"))
print(countBool("boolean a = true,b,c,d,e;"))

