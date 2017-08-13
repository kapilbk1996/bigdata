#!/usr/bin/python2

import cgi
import commands

print "Content-Type: text/html"
print 

actionIp=cgi.FormContent()['actionIp'][0]
outDir=cgi.FormContent()['outDir'][0]

f=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} hadoop fs -cat {}/part-00000".format(actionIp,outDir))

print """
<br />
<br />
<br />
"""
print f[1]
