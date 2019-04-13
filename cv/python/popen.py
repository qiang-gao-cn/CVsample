#!/usr/bin/python
#_*_ coding:UTF-8 _*_
import os
cmd = 'mkdir nwdir'
a = os.popen(cmd)
print(a)
print(type(a))
print("-------------------------")
cmd = 'touch a.txt'
a = os.popen(cmd)
print(a)
print(type(a))
path = "/home/vagrant"
for i in  os.listdir(path):
	#if os.path.isdir(i):
	if os.path.isfile(i):
		print(i)
