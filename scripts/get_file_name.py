#!/usr/bin/python2

import cgi
import commands

print "content-type: text/html"
print 

fn=cgi.FormContent()['fn'][0]
fh=open('file_name.txt', 'w')
fh.write(fn)
fh.close()

