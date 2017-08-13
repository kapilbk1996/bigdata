#!/usr/bin/python2

import cgi
import commands

print "Content-Type: text/html"
print 


fileName=cgi.FormContent()['fileName'][0]
productType=cgi.FormContent()['productType'][0]
payType=cgi.FormContent()['payType'][0]
reducerType=cgi.FormContent()['reducerType'][0]
actionIp=cgi.FormContent()['actionIp'][0]
outDir=cgi.FormContent()['outDir'][0]


mapperContent="""#!/usr/bin/python2

import re
import sys
for i in sys.stdin:
	j=i.strip()
	k=j.split('\\r')
	t=k[0]
	d=t.split(',')
	#price=d[2]
	product=d[1]
	payType=d[3]
	#print price
	if product=='{}' and payType=='{}':
		print i,
	else:
		pass		


""".format(productType,payType)


f=open("/webcontent/scripts/demoMapper1.py",'w')
f.write(mapperContent)
f.close()

if reducerType=='view':
	reducerContent="""#!/usr/bin/python2

import re
import sys

#print 'Content-Type: text/html'

print "<div align='center' >"
print "<table border='5'>"
print "<tr><th>Date</th><th>Product</th><th>Price</th><th>Payment Mode </th><th>Name</th><th>City</th><th>State</th><th>Country</th><th>Account created</th></tr>"
for i in sys.stdin:
	t=i.split(',')
	print "<tr><td>" + t[0] + "</td><td>" + t[1] + "</td><td>" + t[2] + "</td><td>" + t[3] + "</td><td>" + t[4] + "</td><td>" + t[5] + "</td><td>" + t[6] + "</td><td>" + t[7] + "</td><td>" + t[8] +"</td></tr>"
print "</table>"
print "</div>"
"""

elif reducerType=='Count':
	reducerContent="""#!/usr/bin/python2
import re
import sys

j=0
for i in sys.stdin:
	j+=1

print "<div align='center' >"
print "<h2>Total count : {}</h2>".format(j)
print "</div>" 
"""


f=open("/webcontent/scripts/demoReducer.py",'w')
f.write(reducerContent)
f.close()




aa="""
---
- hosts: myhost
  tasks:
  - copy:
     src: '/webcontent/scripts/demoMapper1.py'
     dest: '/'
  - copy:
     src: '/webcontent/scripts/demoReducer.py'
     dest: '/'  
"""
f=open("/webcontent/scripts/noUse.yml",'w')
f.write(aa)
f.close()

commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
		
inventoryContent="[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(actionIp)
fstabfh=open('/etc/ansible/hosts','w')
fstabfh.write(inventoryContent)
fstabfh.close()	

commands.getstatusoutput("sudo ansible-playbook /webcontent/scripts/noUse.yml")

ss=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {2} hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input {0} -mapper ./demoMapper1.py -file /demoMapper1.py -reducer ./demoReducer.py -file /demoReducer.py -output {1}".format(fileName,outDir,actionIp))
if ss[0]==0:
	print """
<br />
<br />
<br />
<br />
<div align='center' >
<h2>Successfully done..</h2>
<br />
<br />
	<a href='mrResult.py?actionIp={}&outDir={}' target='_blank' >view output<a/>

<br />
<br />
<br />
<a href='../docker_mr_programs.html' >Run another map-reduce program</a> | 
<a href='../index.html' >Home</a>
</div>
""".format(actionIp,outDir)
	#print "sdsD"
	#f=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} hadoop fs -cat {}/part-00000".format(actionIp,outDir))

	#print f[1]

else:
	print ss[1]
	
