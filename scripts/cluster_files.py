#!/usr/bin/python2

import cgi
import commands
import re



def fileNames(actionIp):
	print "<select id='fileName'>"
	print "<option>Select</option>"
	d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} hadoop fs -ls /".format(actionIp))

	for i in d[1].split("\n"):
		if re.search("Failed to add the host to the",i) or re.search("Found [0-9] items",i) or re.search("Could not create directory",i):
		  pass
		
		else:
		  filenamee= i.split(" ")[-1]
		  print "<option>{}</option>".format(filenamee)	
	print "</select>"

#fileNames('192.168.1.5')
