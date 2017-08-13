#!/usr/bin/python2

import re
import sys
for i in sys.stdin:
	j=i.strip()
	k=j.split('\r')
	t=k[0]
	d=t.split(',')
	#price=d[2]
	product=d[1]
	payType=d[3]
	#print price
	if product=='Product2' and payType=='Mastercard':
		print i,
	else:
		pass		


