#!/usr/bin/python2

import commands
import cgi

print "Content-Type: text/html"
print

actionIp=cgi.FormContent()['actionIp'][0]
fName=cgi.FormContent()['fileName'][0]

#script to view error log on web

d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} hadoop fs -rm {}".format(actionIp,fName))

if d[0]!=0:
	d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} hadoop fs -rmr {}".format(actionIp,fName))
	

g=d[1]

print """
<script>
 function err(){
"""
print 'alert("' + g +'");'

print """

}

</script>
"""


if d[0]==0:
	print  """
<br />
<br />
<br />
<div align='center' >
<h2><u>'{}'</u> : File removed SUCCESSFULLY !!!</h2>
<br />
<br />
<a href='file_remove.py?actionIp={}' >Remove another file</a> | 

<a href='../index.html' >Home</a>




</div>

""".format(fName,actionIp)

else:
	print """
<br />
<br />
<br />
<div align='center' >
<h1>ERROR :(</h1> 
<br />
<br />
<input type='submit' onclick=err() value='View error' >
<br />
<br />
<a href='../index.html' >Home</a>

</div>

"""


