#!/usr/bin/python2
import os
import commands
import cgi

print "Content-Type: text/html"
print

uName=cgi.FormContent()["user"][0]

uPass=cgi.FormContent()["pass"][0]
print uPass +" "+ uName


if uName =='guest' and uPass =='kapil':
  print "allowed"

else:
  print "Not Allowed"
  

