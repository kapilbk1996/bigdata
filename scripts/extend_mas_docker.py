#!/usr/bin/python2

import cgi
import commands

print "content-type: text/html"
print

userName=cgi.FormContent()['userName'][0]
hostIp=cgi.FormContent()['actionIp'][0]
extendBy=cgi.FormContent()['extendBy'][0]
partSize=cgi.FormContent()['partSize'][0]



d=commands.getstatusoutput("ifconfig enp0s3 | grep inet")
myipp=d[1].split()[1]


commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
		
inventoryContent="[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)
inventoryContent=inventoryContent + "[currenthost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(myipp)
fstabfh=open('/etc/ansible/hosts','w')
fstabfh.write(inventoryContent)
fstabfh.close()	
#print 'Inventory file made <br />'



############# to create lv and mount them

k=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} docker ps | grep {}-*".format(hostIp,userName))

sj=k[1].split("\n")
t=[]
for i in sj:
	d=i.split(" ")
	t.append( d[-1])
kkk=t[-2].split("-")[-1]

#print kk
kk=int(kkk)


i=1

lvSetup="---\n- hosts: myhost\n  tasks:\n"
while i<= int(extendBy):
	
	nk=kk+i
	lvSetup=lvSetup+"  - lvol:\n     lv: '{0}-lv{2}'\n     vg: 'myvg'\n     size: '{1}g'\n  - parted:\n     device: '/dev/myvg/{0}-lv{2}'\n  - filesystem:\n     fstype: ext4\n     dev: '/dev/myvg/{0}-lv{2}'\n  - file:\n     state: directory\n     path: '/share/{0}-lv{2}'\n  - mount:\n     path: '/share/{0}-lv{2}'\n     state: mounted\n     src: '/dev/myvg/{0}-lv{2}'\n     fstype: ext4\n".format(userName,partSize,nk)
	i+=1
f=open('/webcontent/scripts/runHere3.yml','w')
f.write(lvSetup)
f.close()
commands.getstatusoutput("sudo chown apache /webcontent/scripts/runHere3.yml")
l=commands.getstatusoutput("sudo ansible-playbook runHere3.yml")
#print 'LVM created <br />'


############### to launch containers 


runDockerContainer="---\n- hosts: myhost\n  tasks:\n"


i=1
while i<=int(extendBy):
	nk=kk+i
	runDockerContainer=runDockerContainer + "  - command: 'docker run -dit --privileged=true -v /share/{0}-lv{1}:/share/{0}-lv{1} --name {0}-{1} hadoopimg:v2'\n".format(userName,nk)
	i+=1


f=open('runHere2.yml','w')
f.write(runDockerContainer)
f.close()	
commands.getstatusoutput("sudo chown apache /webcontent/scripts/runHere2.yml")
j=commands.getstatusoutput("sudo ansible-playbook runHere2.yml")
#print j
#print 'containers launched <br />'



############# to get I/P of dockers
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

#to get master Ip

d=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} docker inspect {1}-0 | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format(hostIp,userName))
ss=d[1]
t=ss.split("\n")
	
ss=ss[:-1]
allIpp.append(ss)


for i in allIpp:
	x=i.split("\n")
	allIp.append(x[-1][1:])

#print allIp


#to create dummy inventory file for host system

i=0
inventoryContent="[slave]\n"
while i<int(extendBy):

	inventoryContent=inventoryContent + "{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[i])
	i+=1

inventoryContent=inventoryContent+"[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)
inventoryContent=inventoryContent+"[master]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[-1])


f=open('/webcontent/scripts/ansi_hosts.txt','w')
f.write(inventoryContent)
f.close()

#print 'dummy inventory file made <br />' 

#create core-site.xml for all

coreSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{}:10001</value>\n</property>\n</configuration>".format(allIp[-1])



h=open('/webcontent/scripts/core-site.xml','w')
h.write(coreSiteContent + "\n")
h.close()

#print "Core site made"

# to create hdfs-site.xml for all slave nodes

i=1
while i<=int(extendBy):
	
	nk=kk+i
	dirName="/share/{}-lv{}".format(userName,nk)
	hdfsSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>{}</value>\n</property>\n</configuration>".format(dirName)
	
	q='/webcontent/scripts/hdfs-site-master{}.xml'.format(nk)
		
	t=open(q,'w')
	t.write(hdfsSiteContent + "\n")
	t.close()	
	
	i+=1
#print "hdfs site made"


## ansible script to be used at host Ip

f="""
---
- hosts: myhost
  tasks:
  
"""
i=1
while i<=int(extendBy):
	
	nk=kk+i
	ff='docker cp /webcontent/scripts/hdfs-site-master{1}.xml {0}-{1}:/etc/hadoop/hdfs-site.xml'.format(userName,nk)
	f=f+ "  - command: '{}'\n".format(ff)
	ff='docker cp /webcontent/scripts/core-site.xml {0}-{1}:/etc/hadoop/core-site.xml'.format(userName,nk)
	f=f+ "  - command: '{}'\n".format(ff)
	ff='docker exec {}-{} hadoop-daemon.sh stop datanode'.format(userName,nk)
	f=f+"  - command: '{}'\n".format(ff)	
	ff='docker exec {}-{} hadoop-daemon.sh start datanode'.format(userName,nk)
	f=f+"  - command: '{}'\n".format(ff)	
	
	i+=1



t=open('/webcontent/scripts/faltu.yml','w')
t.write(f + "\n")
t.close()	

#print "faltu made"
### ansible script to be used at current ip


s="""

---
- hosts: myhost
  tasks:
  - copy:
     src: '/webcontent/scripts/core-site.xml'
     dest: '/webcontent/scripts/'
  - copy:
     src: '/webcontent/scripts/ansi_hosts.txt'
     dest: '/etc/ansible/hosts'
  - copy:
     src: '/webcontent/scripts/faltu.yml'
     dest: '/webcontent/scripts/'  

"""

i=1
while i<=int(extendBy):
	
	nk=kk+i
	s=s+"  - copy:\n      src: '/webcontent/scripts/hdfs-site-master{}.xml'\n      dest: '/webcontent/scripts/'\n".format(nk)	
	i+=1
	
s=s+"  - command: 'sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} ansible-playbook /webcontent/scripts/faltu.yml'\n".format(hostIp)

h=open('/webcontent/scripts/noUse.yml','w')
h.write(s)
h.close()

#print "noUse made"

#run noUse.yml

commands.getstatusoutput("sudo chown apache /webcontent/scripts/noUse.yml")
dd=commands.getstatusoutput('sudo ansible-playbook noUse.yml')


commands.getoutput("rm /webcontent/scripts/core-site.xml")
commands.getoutput("echo y | rm /webcontent/scripts/noUse.yml")
commands.getoutput("rm /webcontent/scripts/faltu.yml")
commands.getoutput("rm /webcontent/scripts/ansi_hosts.txt")

i=1
while i<= int(totalSlave):

	nk=kk+i
	commands.getoutput("echo y | rm /webcontent/scripts/hdfs-site-master{}.xml".format(nk))
	i+=1


yy=int(extendBy)
lkj=yy+kk
print """
<br />
<br />
<br />

<div align='center' >
<h2>Successfully done !!!</h2>
<br />
<h3>Cluster extended by {0} nodes
<br />
Total nodes = {1}</h3>
<br />
<br />
<br />
<a href='../index.html' >Home</a>
</div>

""".format(extendBy,lkj)

print "done"
