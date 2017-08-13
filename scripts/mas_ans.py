#!/usr/bin/python2

import os
import commands
import cgi
import thread

print "Content-Type: text/html"
print 

masterIp=cgi.FormContent()['masterIp'][0]	#"192.168.1.7"
dirName=cgi.FormContent()['dirName'][0]	#"/ansi_test"#
slaveIp=cgi.FormContent()['slaveIp'][0]#"192.168.1.6"#
partSize=cgi.FormContent()['partSize'][0]#"1"#
userName=cgi.FormContent()['userName'][0]#"ansi_guest"#


     	
####### Task - 1 : check softwares | configure core-site.xml in all nodes 
commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
		
inventoryContent="[master]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n[slave]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(masterIp,slaveIp)
fstabfh=open('/etc/ansible/hosts','a')
fstabfh.write(inventoryContent)
fstabfh.close()	

coreSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{}:10001</value>\n</property>\n</configuration>".format(masterIp)

commands.getstatusoutput("sudo chown apache /webcontent/scripts")

h=open('/webcontent/scripts/core-site.xml','w')
h.write(coreSiteContent + "\n")
h.close()	

forAll="""
---
- hosts: all
  tasks:
  - package:
     name: 'hadoop'
     state: present

  - package:
     name: 'jdk'
     state: present

  - copy:
     src: '/webcontent/scripts/core-site.xml'
     dest: '/etc/hadoop/'

"""
f=open('/webcontent/scripts/noUse.yml','w')
f.write(forAll)
f.close()

k=commands.getstatusoutput("sudo ansible-playbook noUse.yml")
print "Task-1 done <br />"
#print k
########## Task - 2 : configure Master node 

hdfsSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>{}</value>\n</property>\n</configuration>".format(dirName)


t=open('/webcontent/scripts/hdfs-site.xml','w')
t.write(hdfsSiteContent + "\n")
t.close()	
		
forMaster="""
---
- hosts: master
  tasks:
  - file:
     path: '{}'
     state: directory
  
  - copy:
     src: '/webcontent/scripts/hdfs-site.xml'
     dest: '/etc/hadoop/'

""".format(dirName)

f=open('noUse.yml','w')
f.write(forMaster)
f.close();

j=commands.getstatusoutput("sudo ansible-playbook noUse.yml")
print "Task-2 done <br />"
#print j
############# Task - 3 : create LVM | mount it | configure Hdfs-site.xml | restart daemons

temp="/share/{}-lv1".format(userName)	
hdfsSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n</configuration>".format(temp)

z=open('/webcontent/scripts/hdfs-site.xml','w')
z.write(hdfsSiteContent + "\n")
z.close()	
		

forSlave="""
---
- hosts: slave
  tasks:
  - lvol: 
     lv: '{0}-lv1'
     vg: 'myvg'
     size: '{1}g'

  - parted:
     device: '/dev/myvg/{0}-lv1'

  - filesystem:
     fstype: ext4
     dev: '/dev/myvg/{0}-lv1'

  - file:
     state: directory
     path: '/share/{0}-lv1'

  - mount:
     path: '/share/{0}-lv1'
     state: mounted
     src: '/dev/myvg/{0}-lv1'
     fstype: ext4

  - copy:
     src: '/webcontent/scripts/hdfs-site.xml'
     dest: '/etc/hadoop/'

  - command: 'hadoop-daemon.sh start datanode'

  
""".format(userName,partSize,dirName)

v=open('noUse1.yml','w')
v.write(forSlave)
v.close();

l=commands.getstatusoutput("sudo ansible-playbook noUse1.yml")

print "Task-3 done <br />"
#print l
######### Task - 4 : format namenode | restart namenode 


v="""
---
- hosts: master
  tasks:
  - command: 'hadoop-daemon.sh stop namenode'
  - command: 'hadoop namenode -format'
  - command: 'hadoop-daemon.sh start namenode'
"""

f=open('noUse.yml','w')
f.write(v)
f.close()

qq=commands.getstatusoutput("sudo ansible-playbook noUse.yml")
print "Task-4 done <br />"
#print qq

#thread.start_new_thread(allMaster,())
#thread.start_new_thread(allSlave,())

commands.getstatusoutput("echo yes | rm /webcontent/scripts/core-site.xml")
commands.getstatusoutput("echo yes | rm /webcontent/scripts/hdfs-site.xml")
commands.getstatusoutput("echo yes | rm /webcontent/hdfs-site.xml")
commands.getstatusoutput("echo yes | rm /webcontent/scripts/noUse.yml")
commands.getstatusoutput("echo yes | rm /webcontent/scripts/noUse1.yml")


	

   	

