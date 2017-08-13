#!/usr/bin/python2
import os
import commands
import cgi

print "Content-Type: text/html"
print


######## Input taken through CGI 
hostIp=cgi.FormContent()['hostIp'][0]
totalTask=cgi.FormContent()['totalTask'][0]
userName=cgi.FormContent()['userName'][0]

d=commands.getstatusoutput("ifconfig enp0s3 | grep inet")
myipp=d[1].split()[1]


commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")
		
inventoryContent="[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)
inventoryContent=inventoryContent + "[currenthost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(myipp)
fstabfh=open('/etc/ansible/hosts','w')
fstabfh.write(inventoryContent)
fstabfh.close()	
#print 'Inventory file made <br />'

############### to launch containers 


runDockerContainer="---\n- hosts: myhost\n  tasks:\n"

runDockerContainer=runDockerContainer + "  - command: 'docker run -dit --privileged=true  --name {0}-00 hadoopimg:v2'\n".format(userName)

f=open('runHere2.yml','w')
f.write(runDockerContainer)
f.close()	
commands.getstatusoutput("sudo chown apache /webcontent/scripts/runHere2.yml")
j=commands.getstatusoutput("sudo ansible-playbook runHere2.yml")
#print j
#print 'containers launched <br />'


############# to get I/P of dockers

if totalTask=="2":
	allIp=['172.17.0.2','172.17.0.3','172.17.0.4']
	jtIp='172.17.0.5'
elif totalTask=="1":
	allIp=['172.17.0.2','172.17.0.3']
	jtIp='172.17.0.4'

elif totalTask=="3":
	allIp=['172.17.0.2','172.17.0.3','172.17.0.4','172.17.0.5 ']
	jtIp='172.17.0.6'


#print "got ip"
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
while i<=int(totalTask):

	inventoryContent=inventoryContent + "{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[i])
	i+=1

inventoryContent=inventoryContent+"[master]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(allIp[0])
inventoryContent=inventoryContent+"[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)
inventoryContent=inventoryContent+"[job]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(jtIp)


f=open('/webcontent/scripts/ansi_hosts.txt','w')
f.write(inventoryContent)
f.close()

#print 'dummy inventory file made <br />' 
#create core-site.xml for job-tracker

coreSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{}:10001</value>\n</property>\n</configuration>".format(allIp[0])



h=open('/webcontent/scripts/core-site.xml','w')
h.write(coreSiteContent + "\n")
h.close()

#to create mapred-site.xml for jobtracker & tasktracker

mapredSiteContent="<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>{}:9001</value>\n</property>\n</configuration>".format(jtIp)


t=open('/webcontent/scripts/mapred-site.xml','w')
t.write(mapredSiteContent + "\n")
t.close()

# store total tasktracker for extending cluster in extend_job_docker.py

df=open("/webcontent/scripts/current_task_count.txt",'w')
df.write(totalTask)
df.close()	
	
## ansible script to be used at host Ip

f='''
---
- hosts: myhost
  tasks:
  - command: "docker cp /webcontent/scripts/mapred-site.xml {0}-00:/etc/hadoop/mapred-site.xml"
  - command: "docker cp /webcontent/scripts/core-site.xml {0}-00:/etc/hadoop/core-site.xml"

'''.format(userName)

i=1
while i<=int(totalTask):

	ff='docker cp /webcontent/scripts/mapred-site.xml {0}-{1}:/etc/hadoop/mapred-site.xml'.format(userName,i)
	f=f+ "  - command: '{}'\n".format(ff)
	ff='docker exec {}-{} hadoop-daemon.sh stop tasktracker'.format(userName,i)
	f=f+"  - command: '{}'\n".format(ff)	
	ff='docker exec {}-{} hadoop-daemon.sh start tasktracker'.format(userName,i)
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
     src: '/webcontent/scripts/mapred-site.xml'
     dest: '/webcontent/scripts/'
  - copy:
     src: '/webcontent/scripts/current_task_count.txt'
     dest: '/webcontent/scripts/'

  - copy:
     src: '/webcontent/scripts/mapred-site.xml'
     dest: '/etc/hadoop/mapred-site.xml'
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

	
s=s+"  - command: 'sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} ansible-playbook /webcontent/scripts/faltu.yml'\n".format(hostIp)

s=s+"  - command: 'docker exec {}-00 hadoop-daemon.sh start jobtracker'".format(userName)

h=open('/webcontent/scripts/noUse.yml','w')
h.write(s)
h.close()
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



commands.getoutput("rm /webcontent/scripts/core-site.xml")
commands.getoutput("rm /webcontent/scripts/current_task_count.txt")
commands.getoutput("rm /webcontent/scripts/mapred-site.xml")
commands.getoutput("rm /webcontent/scripts/runHere2.yml")
commands.getoutput("rm /webcontent/scripts/noUse.yml")
commands.getoutput("rm /webcontent/scripts/faltu.yml")
commands.getoutput("rm /webcontent/scripts/ansi_hosts.txt")



