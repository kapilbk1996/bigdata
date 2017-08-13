#!/usr/bin/python2
import os
import commands
import cgi

print "Content-Type: text/html"
print

lvSetup="  - lvol:\n     lv: '{0}-lv{2}'\n     vg: 'myvg'\n     size: '{1}g'\n  - parted:\n     device: '/dev/myvg/{0}-lv{2}'\n  - filesystem:\n     fstype: ext4\n     dev: '/dev/myvg/{0}-lv{2}'\n  - file:\n     state: directory\n     path: '/share/{0}-lv{2}'\n  - mount:\n     path: '/share/{0}-lv{2}'\n     state: mounted\n     src: '/dev/myvg/{0}-lv{2}'\n     fstype: ext4\n".format('bhola','1','1')
	#i+=1
#print "sdsd"
f=open('/webcontent/scripts/runHere3.yml','w')
#print "mmmm"
f.write(lvSetup)
f.close()
