#!/usr/bin/python2
import os
import commands
import cgi

print "Content-Type: text/html"
print

#print "LLL"

######## Input taken through CGI 
userName=cgi.FormContent()['userName'][0]
totalSlave=cgi.FormContent()['totalSlave'][0]
hostIp=cgi.FormContent()['hostIp'][0]
partSize=cgi.FormContent()['partSize'][0]


#print "jjlj"
#print "{}<br />".format(userName)
#print "{}<br />".format(totalSlave)
#print "{}<br />".format(hostIp)
#print "{}<br />".format(partSize)



#print totalSlave

commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
		
inventoryContent="[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)
inventoryContent=inventoryContent + "[currenthost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format("192.168.1.5")
fstabfh=open('/etc/ansible/hosts','w')
fstabfh.write(inventoryContent)
fstabfh.close()	
print 'Inventory file made <br />'

########### to restart docker
runDockerService='''
---
- hosts: myhost
  tasks:
  - command: 'systemctl start docker'
'''
commands.getstatusoutput("sudo chown apache /webcontent/scripts")
f=open('runHere1.yml','w')
f.write(runDockerService)
f.close();

commands.getstatusoutput("sudo chown apache /webcontent/scripts/runHere1.yml")
j=commands.getstatusoutput("sudo ansible-playbook runHere1.yml")
print "Docker service started <br />"
############# to create lv and mount them

i=1
lvSetup="---\n- hosts: myhost\n  tasks:\n"
while i<= int(totalSlave):
	
	lvSetup=lvSetup+"  - lvol:\n     lv: '{0}-lv{2}'\n     vg: 'myvg'\n     size: '{1}g'\n  - parted:\n     device: '/dev/myvg/{0}-lv{2}'\n  - filesystem:\n     fstype: ext4\n     dev: '/dev/myvg/{0}-lv{2}'\n  - file:\n     state: directory\n     path: '/share/{0}-lv{2}'\n  - mount:\n     path: '/share/{0}-lv{2}'\n     state: mounted\n     src: '/dev/myvg/{0}-lv{2}'\n     fstype: ext4\n".format(userName,partSize,i)
	i+=1
#print "sdsd"
f=open('/webcontent/scripts/runHere3.yml','w')
#print "mmmm"
f.write(lvSetup)
f.close()
#print "fdfdfd"
#commands.getstatusoutput("sudo chown apache /webcontent/scripts/runHere.yml")
commands.getstatusoutput("sudo chown apache /webcontent/scripts/runHere3.yml")
#print "oooo"
l=commands.getstatusoutput("sudo ansible-playbook runHere3.yml")
print 'LVM created <br />'

############### to launch containers 


runDockerContainer="---\n- hosts: myhost\n  tasks:\n"

i=0
while i<=int(totalSlave):

	runDockerContainer=runDockerContainer + "  - command: 'docker run -dit --privileged=true -v /share/{0}-lv{1}:/share/{0}-lv{1} --name {0}-{1} hadoopimg:v2'\n".format(userName,i)
	i+=1


f=open('runHere2.yml','w')
f.write(runDockerContainer)
f.close()	
commands.getstatusoutput("sudo chown apache /webcontent/scripts/runHere2.yml")
j=commands.getstatusoutput("sudo ansible-playbook runHere2.yml")
#print j
print 'containers launched <br />'


############# to get I/P of dockers

if totalSlave=="2":
	allIp=['172.17.0.2','172.17.0.3','172.17.0.4']
elif totalSlave=="1":
	allIp=['172.17.0.2','172.17.0.3']

elif totalSlave=="3":
	allIp=['172.17.0.2','172.17.0.3','172.17.0.4','172.17.0.5 ']

'''
i=0
while i<=int(totalSlave):

	d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} docker inspect {1}-{2} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format(hostIp,userName,i))
	print "lLL"
	print d
	print "asdasd"
	ss=d[1]
	t=ss.split("\n")
	
	ss=ss[1:-1]
	allIp.append(ss)
	i+=1
'''
#print allIp

#to create dummy inventory file for host system

i=1
inventoryContent="[slave]\n"
while i<=int(totalSlave):

	inventoryContent=inventoryContent + "{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[i])
	i+=1

inventoryContent=inventoryContent+"[master]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[0])
inventoryContent=inventoryContent+"[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)


f=open('/webcontent/scripts/ansi_hosts.txt','w')
f.write(inventoryContent)
f.close()

print 'dummy inventory file made <br />' 
#create core-site.xml for all

coreSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{}:10001</value>\n</property>\n</configuration>".format(allIp[0])



h=open('/webcontent/scripts/core-site.xml','w')
h.write(coreSiteContent + "\n")
h.close()

#to create hdfs-site.xml for master

dirName="/" + userName + "Master"
hdfsSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>{}</value>\n</property>\n</configuration>".format(dirName)


t=open('/webcontent/scripts/hdfs-site-master.xml','w')
t.write(hdfsSiteContent + "\n")
t.close()	
	
# to create hdfs-site.xml for all slave nodes

i=1
while i<=int(totalSlave):
	
	dirName="/share/{}-lv{}".format(userName,i)
	hdfsSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n</configuration>".format(dirName)
	
	q='/webcontent/scripts/hdfs-site-master{}.xml'.format(i)
		
	t=open(q,'w')
	t.write(hdfsSiteContent + "\n")
	t.close()	
	
	i+=1
	

## ansible script to be used at host Ip

f='''
---
- hosts: myhost
  tasks:
  - command: "docker cp /webcontent/scripts/hdfs-site-master.xml {0}-0:/etc/hadoop/hdfs-site.xml"
  - command: "docker cp /webcontent/scripts/core-site.xml {0}-0:/etc/hadoop/core-site.xml"

'''.format(userName)

i=1
while i<=int(totalSlave):

	ff='docker cp /webcontent/scripts/hdfs-site-master{1}.xml {0}-{1}:/etc/hadoop/hdfs-site.xml'.format(userName,i)
	f=f+ "  - command: '{}'\n".format(ff)
	ff='docker cp /webcontent/scripts/core-site.xml {0}-{1}:/etc/hadoop/core-site.xml'.format(userName,i)
	f=f+ "  - command: '{}'\n".format(ff)
	ff='docker exec {}-{} hadoop-daemon.sh stop datanode'.format(userName,i)
	f=f+"  - command: '{}'\n".format(ff)	
	ff='docker exec {}-{} hadoop-daemon.sh start datanode'.format(userName,i)
	f=f+"  - command: '{}'\n".format(ff)	
	
	i+=1



t=open('/webcontent/scripts/faltu.yml','w')
t.write(f + "\n")
t.close()	



### ansible script to be used at current ip


s='''

---
- hosts: myhost
  tasks:
  - copy:
     src: '/webcontent/scripts/hdfs-site-master.xml'
     dest: '/webcontent/scripts/'
  - copy:
     src: '/webcontent/scripts/core-site.xml'
     dest: '/webcontent/scripts/'
  - copy:
     src: '/webcontent/scripts/ansi_hosts.txt'
     dest: '/etc/ansible/hosts'
  - copy:
     src: '/webcontent/scripts/faltu.yml'
     dest: '/webcontent/scripts/'  

'''

i=1
while i<=int(totalSlave):
	
	s=s+"  - copy:\n      src: '/webcontent/scripts/hdfs-site-master{}.xml'\n      dest: '/webcontent/scripts/'\n".format(i)	
	i+=1
	
s=s+"  - command: 'sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} ansible-playbook /webcontent/scripts/faltu.yml'\n".format(hostIp)

s=s+"  - command: 'docker exec {}-0 hadoop namenode -format'\n".format(userName)
s=s+"  - command: 'docker exec {}-0 hadoop-daemon.sh start namenode'".format(userName)

h=open('/webcontent/scripts/noUse.yml','w')
h.write(s)
h.close()
commands.getstatusoutput("sudo chown apache /webcontent/scripts/noUse.yml")
dd=commands.getstatusoutput('sudo ansible-playbook noUse.yml')


gg=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} docker exec {1}-0 mkdir /{1}Master".format(hostIp,userName))




print "<h2>Successfully done</h2>"



commands.getoutput("rm /webcontent/scripts/core-site.xml")
commands.getoutput("rm /webcontent/scripts/hdfs-site-master.xml")
commands.getoutput("rm /webcontent/scripts/runHere3.yml")
commands.getoutput("rm /webcontent/scripts/runHere2.yml")
commands.getoutput("rm /webcontent/scripts/runHere1.yml")
commands.getoutput("rm /webcontent/scripts/noUse.yml")
commands.getoutput("rm /webcontent/scripts/faltu.yml")
commands.getoutput("rm /webcontent/scripts/ansi_hosts.txt")

i=1
while i<= int(totalSlave):
	commands.getoutput("rm /webcontent/scripts/hdfs-site-master{}.xml".format(i))
	i+=1

"""

ff='docker exec {}-0 hadoop namenode -format'.format(userName)	
f=f+"  - command: '{}'\n".format(ff)	

ff='docker exec {}-0 hadoop-daemon.sh stop namenode'.format(userName)	
f=f+"  - command: '{}'\n".format(ff)	


ff='docker exec {}-0 hadoop-daemon.sh start namenode'.format(userName)	
f=f+"  - command: '{}'\n".format(ff)	

	

"""
