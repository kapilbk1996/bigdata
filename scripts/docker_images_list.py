#!/usr/bin/python2


import commands
import re



def docker_list(hostIp):
	print "<select name='imagename'>"
	for i in commands.getoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} docker images".format(hostIp)).split('\n'):
		if re.search("Failed to add",i) or re.search("REPOSITORY",i) or re.search("Could not create directory",i):	
			pass
		else:
			j=i.split()
			print "<option>" + j[0] + ":" + j[1] + "</option>"

	print "</select>"



#docker_list("192.168.1.5")
