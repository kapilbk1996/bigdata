#!/usr/bin/python2

import commands
import cgi
import cluster_files
import re

print "content-type: text/html"
print 


actionIp=cgi.FormContent()['actionIp'][0]
fileName=cgi.FormContent()['fileName'][0]
outDir=cgi.FormContent()['outDir'][0]

print """
<br />
<br />
<br />
<div align='center'>
<h2>WordCount job</h2>
<h3>File name : <u>{0}</u>
<br />
Client Ip : <u>{1}</u>
</h3>
<br />
<br />
<br />
<a href='../index.html'>Home</a> 
<br />
<br />

""".format(fileName,actionIp)
f=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {2} hadoop jar /usr/share/hadoop/hadoop-examples-1.2.1.jar wordcount {0} {1}".format(fileName,outDir,actionIp))


if f[0]==0:
	d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} hadoop fs -cat {1}/part-r-00000".format(actionIp,outDir))
	totalCount=f[1].split("=")[-1]
	print "<h2>Total word count = {}</h2>".format(totalCount)
	print """
<br />
<br />
<table>
"""
	for i in d[1].split("\n"):
		if re.search("Could not create directory",i) or re.search("Failed to add the host",i):
		  	pass
		else:
			j=i.split("\t")
			print "<tr><td>{}</td> <td>----> </td><td>{}</td></tr>".format(j[0],j[1])

print """
</table>
<br />
<br />
<br />
</div>

"""



	
