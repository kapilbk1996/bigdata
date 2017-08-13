#!/usr/bin/python2

import commands
import cgi

print "content-type: text/html"

cName=cgi.FormContent()['x'][0]
actionIp=cgi.FormContent()['actionIp'][0]


if cName == "allall":
	cremovestatus=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {}   docker rm -f $(docker ps -aq)".format(actionIp))
	
else:
	cremovestatus=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {1} docker rm -f {0}".format(cName,actionIp))

print "location:  docker_manage.py?actionIp={}".format(actionIp)
print 

