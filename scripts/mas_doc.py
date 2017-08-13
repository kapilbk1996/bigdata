#!/usr/bin/python2
import os
import commands
import cgi
import thread

print "Content-Type: text/html"
print

######## Input taken through CGI 
totalSlave='2'
partSize="1"#cgi.FormContent()['partSize'][0]
userName="ansi_guest"#cgi.FormContent()['userName'][0]
hostIp="192.168.1.6"



runDockerService="""
---
- hosts: myhost
  tasks:
  - command: 'systemctl start docker'
"""
f=open('noUse.yml','w')
f.write(runDockerService)
f.close();

j=commands.getstatusoutput("sudo ansible-playbook noUse.yml")
#print j

runDockerContainer="---\n- hosts: myhost\n  tasks:\n"

i=0
while i<=int(totalSlave):

	runDockerContainer=runDockerContainer + "  - command: 'docker run -dit --privileged=true --name {}-{} hadoopimg:v2'\n".format(userName,i)
	i+=1


f=open('noUse.yml','w')
f.write(runDockerContainer)
f.close()	

j=commands.getstatusoutput("sudo ansible-playbook noUse.yml")
#print j


allIp=[]
i=0
while i<=int(totalSlave):

	d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root 192.168.1.6 docker inspect {}-{} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format(userName,i))
	ss=d[1]
	ss=ss[1:-1]
	allIp.append(ss)
	i+=1


#print allIp


i=1
while i<= int(totalSlave):
	
	lvSetup="---\n- hosts: slave\n  tasks:\n  - lvol:     lv: '{0}-lv{2}'\n     vg: 'myvg'\n     size: '{1}g'\n  - parted:\n     device: '/dev/myvg/{0}-lv{2}'\n  - filesystem:\n     fstype: ext4\n     dev: '/dev/myvg/{0}-lv{2}'\n  - file:\n     state: directory\n     path: '/share/{0}-lv{2}'\n  - mount:\n     path: '/share/{0}-lv{2}'\n     state: mounted\n     src: '/dev/myvg/{0}-lv{2}'\n     fstype: ext4\n".format(userName,partSize,i)
	
	f=open('/webcontent/scripts/noUsee.yml','w')
	f.write(forMaster)
	f.close()

	


     	
coreSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{}:10001</value>\n</property>\n</configuration>".format(allIp[0])



h=open('/webcontent/scripts/core-site.xml','w')
h.write(coreSiteContent + "\n")
h.close()

dirName="/" + userName + "Master"
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
     src: '/webcontent/scripts/core-site.xml'
     dest: '/etc/hadoop'
  - copy:
     src: '/webcontent/scripts/hdfs-site.xml'
     dest: '/etc/hadoop'
""".format(dirName)
f=open('/webcontent/scripts/noUsee.yml','w')
f.write(forMaster)
f.close()

i=1
inventoryContent="[slave]\n"
while i<=int(totalSlave):

	inventoryContent=inventoryContent + "{} ansible_ssh_user=root  ansible_ssh+pass=redhat\n".format(allIp[i])
	i+=1

inventoryContent=inventoryContent+"[master]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[0])
inventoryContent=inventoryContent+"[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)


f=open('/webcontent/scripts/ansi_hosts.txt','w')
f.write(inventoryContent)
f.close()	



tempp="""
---
- hosts: all
  tasks:  
  - copy:
     src: '/webcontent/scripts/core-site.xml'
     dest: '/webcontent/scripts'
  - copy:
     src: '/webcontent/scripts/hdfs-site.xml'
     dest: '/webcontent/scripts'
  - copy:
     src: '/webcontent/scripts/noUsee.yml'
     dest: '/webcontent/scripts'
  - copy:
     src: '/webcontent/scripts/ansi_hosts.txt'
     dest: '/webcontent/scripts'
  

"""
f=open('/webcontent/scripts/noUse.yml','w')
f.write(tempp)
f.close()

k=commands.getstatusoutput("sudo ansible-playbook noUse.yml")
#print k


commands.getstatusoutput("echo yes | rm /webcontent/scripts/core-site.xml")
commands.getstatusoutput("echo yes | rm /webcontent/scripts/ansi_hosts.txt")
commands.getstatusoutput("echo yes | rm /webcontent/scripts/noUsee.yml")


tempp="""
---
- hosts: all
  tasks:  
  - command: "sudo ansible-playbook /webcontent/scripts/noUsee.yml -i /webcontent/scripts/ansi_hosts.txt"
     
"""
f=open('/webcontent/scripts/noUse.yml','w')
f.write(tempp)
f.close()
k=commands.getstatusoutput("sudo ansible-playbook noUse.yml")
#print k

###############################

temp="/share/{}-lv".format(userName)	
hdfsSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n</configuration>".format(temp)

z=open('/webcontent/scripts/hdfs-site.xml','w')
z.write(hdfsSiteContent + "\n")
z.close()

forSlave="""
---







""".format(dirName)
f=open('/webcontent/scripts/noUsee.yml','w')
f.write(forSlave)
f.close()
	
		
tempp="""
---
- hosts: all
  tasks:  
  - copy:
     src: '/webcontent/scripts/hdfs-site.xml'
     dest: '/webcontent/scripts'
  - copy:
     src: '/webcontent/scripts/noUsee.yml'
     dest: '/webcontent/scripts'
"""
f=open('/webcontent/scripts/noUse.yml','w')
f.write(tempp)
f.close()
k=commands.getstatusoutput("sudo ansible-playbook noUse.yml")





raw_input("EXIT")
