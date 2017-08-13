#!/usr/bin/python2

import re
import sys
inputt ='00:00-03:00'
for i in sys.stdin:
	j=i.strip()
	k=j.split('\r')
	t=k[0]
	d=t.split(',')
	#price=d[2]
	product=d[1]
	payType=d[3]
	transTime=d[0]
	#print price
	if product=='Product2' and payType=='Mastercard':
		#print transTime
		newTime=transTime.split()
		#print newTime
		time=newTime[1]
#		print time
		finalTime=time.split(":")
		#print finalTime
		hrs=finalTime[0]
	 	minutes=finalTime[1]
		w=inputt.split("-")
		firstHrs=w[0].split(":")[0]
		secondHrs=w[1].split(":")[0]
		firstMin=w[0].split(":")[1]
		secondMin=w[1].split(":")[1]
		
		if hrs>=firstHrs and hrs<secondHrs:
			print i,
		elif hrs==secondHrs and secondMin>minutes:
			print i,
		else:
		 	pass
	else:
		pass		





















'''
t=transTime.split()
	 hours=t[1]
	 hourss=hours.split(":")
	 h=hourss[0]	 
	 m=hourss[1]
	 dd=inputt.split("-")
	 #print dd

	 firstHrs=dd[0].split(":")[0]
	 firstMin=dd[0].split(":")[1]
	 secondHrs=dd[1].split(":")[0]
	 secondMin=dd[1].split(":")[1]
	 #print firstHrs
	 #print i
	 
	 if h>=firstHrs and h<secondHrs :
	   print i,
	 elif h==secondHrs and secondMin>m:
	   print i,
	   
	 else:
	   pass
	else:
	 pass

'''

