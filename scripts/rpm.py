#!/usr/bin/python2

import commands
import cgi

print "Content-Type: text/html"
print

packageName=cgi.FormContent()['rpm'][0]
ipAddress=cgi.FormContent()['ip'][0]


status=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} yum install {} -y".format(ipAddress,packageName))
if status[0]==0:
  print "software installed SUCCESSFULLY.. "
else:
  print "software not installed.."


