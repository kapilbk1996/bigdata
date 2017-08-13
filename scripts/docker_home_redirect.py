#!/usr/bin/python2

import cgi

print "content-type: text/html"


actionIp=cgi.FormContent()['actionIp'][0]
imageName=cgi.FormContent()['imagename'][0]
cName=cgi.FormContent()['cName'][0]

x=imageName.split(":")


print "location:  docker_launch.py?actionIp={}&imagename={}%3A{}&cName={}".format(actionIp,x[0],x[1],cName)
print


