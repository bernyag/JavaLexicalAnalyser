#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from byte import *
from short import *

print(countByte("byte a=4, b, c ;"))
print(countByte("byte a=569, b, ;")) # Fail out of range
print(countByte("byte[ ] a={10}, b, c ;"))
print(countShort("short a=1000, b, c ;"))
print(countShort("short a=5, b, ;"))
print(countShort("short[ ] a={78 , 90}, b, c ;"))

