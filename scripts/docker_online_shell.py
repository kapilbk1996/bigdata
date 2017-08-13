#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"

actionIp=cgi.FormContent()['actionIp'][0]


d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} rpm -q shellinabox".format(actionIp))

if d[0]==0:
	commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} systemctl restart shellinaboxd".format(actionIp))
	
	print "location:  https://{}:4200".format(actionIp)
	print 

else:
	print 
	print """
<br />
<br />
<br />
<div align='center' >

"""
	print "<h2><u>shellinabox</u> package not installed at <u>{}</u></h2><br /><h3>Install it manually then try again..</h3><br /><br />".format(actionIp)
	print "<a href='../index.html'>Home</a>".format(actionIp)

print "</div>"
