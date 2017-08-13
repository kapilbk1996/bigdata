#!/usr/bin/python2

import cgi
import commands

print "content-type: text/html"
print


userName=cgi.FormContent()['userName'][0]
hostIp=cgi.FormContent()['actionIp'][0]
extendBy=cgi.FormContent()['extendBy'][0]
'''

userName="tkss"
hostIp='192.168.1.4'
extendBy='2'
'''

ss=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} cat /webcontent/scripts/current_task_count.txt".format(hostIp))

currentTask=ss[1][-1]

#get my system ip
d=commands.getstatusoutput("ifconfig enp0s3 | grep inet")
myipp=d[1].split()[1]


commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
		
inventoryContent="[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)
inventoryContent=inventoryContent + "[currenthost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(myipp)
fstabfh=open('/etc/ansible/hosts','w')
fstabfh.write(inventoryContent)
fstabfh.close()	
print 'Inventory file made <br />'

############# to get I/P of dockers

kk=int(currentTask)

allIpp=[]
allIp=[]

i=1
while i<=int(extendBy):

	nk=kk+i
	d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} docker inspect {1}-{2} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format(hostIp,userName,nk))
	ss=d[1]
	t=ss.split("\n")
	
	ss=ss[:-1]
	allIpp.append(ss)
	i+=1

d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} docker inspect {1}-00 | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format(hostIp,userName))
ss=d[1]
t=ss.split("\n")
	
ss=ss[:-1]
allIpp.append(ss)



for i in allIpp:
	x=i.split("\n")
	allIp.append(x[-1][1:])

print  allIp

#to create dummy inventory file for host system

i=0
inventoryContent="[slave]\n"
while i<int(extendBy):

	inventoryContent=inventoryContent + "{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[i])
	i+=1

inventoryContent=inventoryContent+"[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)

f=open('/webcontent/scripts/ansi_hosts.txt','w')
f.write(inventoryContent)
f.close()

print 'dummy inventory file made <br />' 

#to create mapred-site.xml for jobtracker & tasktracker

mapredSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>{}:9001</value>\n</property>\n</configuration>".format(allIp[-1])


t=open('/webcontent/scripts/mapred-site.xml','w')
t.write(mapredSiteContent + "\n")
t.close()

print "mapred-site made"

## ansible script to be used at host Ip

f='''
---
- hosts: myhost
  tasks:
'''

i=1
while i<=int(extendBy):

	nk=kk+i
	ff='docker cp /webcontent/scripts/mapred-site.xml {0}-{1}:/etc/hadoop/mapred-site.xml'.format(userName,nk)
	f=f+ "  - command: '{}'\n".format(ff)
	ff='docker exec {}-{} hadoop-daemon.sh stop tasktracker'.format(userName,nk)
	f=f+"  - command: '{}'\n".format(ff)	
	ff='docker exec {}-{} hadoop-daemon.sh start tasktracker'.format(userName,nk)
	f=f+"  - command: '{}'\n".format(ff)	
	
	i+=1



t=open('/webcontent/scripts/faltu.yml','w')
t.write(f + "\n")
t.close()	

print "faltu made"

### ansible script to be used at current ip

s='''

---
- hosts: myhost
  tasks:
  - copy:
     src: '/webcontent/scripts/mapred-site.xml'
     dest: '/webcontent/scripts/'
  - copy:
     src: '/webcontent/scripts/ansi_hosts.txt'
     dest: '/etc/ansible/hosts'
  - copy:
     src: '/webcontent/scripts/faltu.yml'
     dest: '/webcontent/scripts/'  

'''

	
s=s+"  - command: 'sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} ansible-playbook /webcontent/scripts/faltu.yml'\n".format(hostIp)


h=open('/webcontent/scripts/noUse.yml','w')
h.write(s)
h.close()

print "nouse made"

commands.getstatusoutput("sudo chown apache /webcontent/scripts/noUse.yml")
dd=commands.getstatusoutput('sudo ansible-playbook noUse.yml')


print """
<br />
<br />
<br />
<br />
<div align='center' >
<h2>Successfully done !!!</h2>
<a href='../index.html' >Home</a>
</div>
"""



