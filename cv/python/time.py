#!/usr/bin/python
#-*- coding:UTF-8 -*-
import time
import calendar
clock1=time.clock()
time1=time.time()
localtime = time.asctime(time.localtime(time.time()))
print("本地时间为：",localtime)
print(time.strftime("%Y%m%d%H%M%S",time.localtime()))
print(time.strftime("%A %B %d %H:%M:%S %Y", time.localtime()))

a = "Sat Mar 28 22:24:24 2016"
print(time.mktime(time.strptime(a,"%a %b %d %H:%M:%S %Y")))

cal = calendar.month(2018,11,6)
print(cal)
clock2=time.clock()
time2=time.time()
print(time2-time1)
print(clock2-clock1)
