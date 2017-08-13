#!/usr/bin/python2


import cgi
import commands

print "content-type: text/html"
print


imageName=cgi.FormContent()['imagename'][0]
cName=cgi.FormContent()['cName'][0]
actionIp=cgi.FormContent()['actionIp'][0]

print """
<br />
<br />
<br />
<div align='center'>

"""

if commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {1} docker inspect {0}".format(cName,actionIp))[0]  == 0:
	print "<h2>{} : this container name <b>already exists </b>at {}</h2><br /><br />".format(cName,actionIp)
	print "<a href='../docker_home.html'>Try another name</a><br />"

else:
	x="docker_manage.py?actionIp={}".format(actionIp)
	commands.getoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {2} docker run  -dit --name {0} {1}".format(cName,imageName,actionIp))
	print "<h2>Container '{}' launched at <b>{}</b></h2><br /><br />".format(cName,actionIp)
	print "<a href='{}'>Click here to manage all container</a> |".format(x)
	print "<a href='../docker_home.html'>Launch another container</a><br />"



print """
</div>
"""


