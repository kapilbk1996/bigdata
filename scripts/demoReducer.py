#!/usr/bin/python2
import re
import sys

j=0
for i in sys.stdin:
	j+=1

print "<div align='center' >"
print "<h2>Total count : {}</h2>".format(j)
print "</div>" 
