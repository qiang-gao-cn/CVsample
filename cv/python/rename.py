#!/usr/bin/python
#-*- coding: UTF-8 _*_
import os
cmd = "ifconfig"
print(os.name)
retval = os.system(cmd)
print(retval)
os.rename("foo2.txt","foo3.txt")
os.remove("foo1.txt")
