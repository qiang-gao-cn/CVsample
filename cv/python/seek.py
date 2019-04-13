#!/usr/bin/python
#-*- coding:UTF-8 _*_
fo = open("foo.txt","rb")
str = fo.read(10)
print("读取的字符串是：",str)
position = fo.tell()
print("当前文件位置：",position)

position = fo.seek(-10,2)
str = fo.read(10)
print("重新读取字符串：",str)
fo.close()

