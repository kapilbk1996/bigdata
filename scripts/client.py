#!/usr/bin/python2

import cgi
import commands

print "content-type: text/html"
print


hostIp=cgi.FormContent()['hostIp'][0]
repFactor=cgi.FormContent()['repFactor'][0]
blockSize=cgi.FormContent()['blockSize'][0]
fileName=cgi.FormContent()['f'][0]


commands.getstatusoutput("sudo chown apache /etc/ansible/hosts")

inventoryContent="[myhost]\n{} ansible_ssh_user=root  ansible_ssh_pass=redhat\n".format(hostIp)
fstabfh=open('/etc/ansible/hosts','w')
fstabfh.write(inventoryContent)
fstabfh.close()	




blockSize=int(blockSize)*1024*1024

f='''
---
- hosts: myhost
  tasks:
  - copy:
     src: '/webcontent/uploads/data.txt'
     dest: '/webcontent/'
  - command: 'mv /webcontent/data.txt /webcontent/{2}'
  - command: 'hadoop fs -Ddfs.replication={0} -Ddfs.block.size={1} -put /webcontent/{2} /'
  - command: 'echo y | rm /webcontent/{2}'
'''.format(repFactor,blockSize,fileName)

h=open('/webcontent/scripts/noUse.yml','w')
h.write(f)
h.close()
commands.getstatusoutput("sudo chown apache /webcontent/scripts/noUse.yml")
dd=commands.getstatusoutput('sudo ansible-playbook /webcontent/scripts/noUse.yml')

commands.getstatusoutput("echo y | rm /webcontent/uploads/data.txt")
print """
<br />
<br />
<br />
<br />
<div align='center'>
<h2>Successfully uploaded <u>'{0}'</u></h2>
<br />
<br />
<a href='../file_upload.html'>Upload another file</a> |
<a href='../index.html'>Home</a>
</div>
""".format(fileName)


