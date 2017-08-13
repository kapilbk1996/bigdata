#!/usr/bin/python2

import cgi
import commands

print "content-type: text/html"

commands.getstatusoutput("sudo chown apache /webcontent/uploads")

fileData=cgi.FormContent()['f'][0]
fh=open('../uploads/data.txt', 'w')
fh.write(fileData)
fh.close()

print "location:  ../upload_redirect.html"
print 

