#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"


cName=cgi.FormContent()['x'][0]
actionIp=cgi.FormContent()['actionIp'][0]

cremovestatus=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {1} docker stop {0}".format(cName,actionIp))

if cremovestatus[0]  == 0:
	print "location:  docker_manage.py?actionIp={}".format(actionIp)
	print
else:
	print "Cannot stop {} at {}".format(cname,actionIp)









