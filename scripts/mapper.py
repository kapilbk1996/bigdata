#!/usr/bin/python2

import re
import sys

jj=0
for i in sys.stdin:
	j=i.strip()
	k=j.split("\r")
	t=k[0]
	d=t.split(",")
	price=d[2]
	product=d[1]
	payType=d[3]
	#print price
	if price == '3600' and product=="Product2" and payType=='Visa':
	 print i,
	 #jj+=1
	else:
	 pass

#print jj
