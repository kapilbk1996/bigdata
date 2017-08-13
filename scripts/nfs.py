#!/usr/bin/python2
import commands
import cgi

print 'Content-Type: text/html'	
print

userName=cgi.FormContent()['userName'][0]
partSize=cgi.FormContent()['partSize'][0]
clientIp=cgi.FormContent()['clientIp'][0]



vgStatus=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} vgdisplay myvg".format(clientIp))
if vgStatus[0]!=0:
   print "myvg not created.. Create  it manually !!!"
   exit()

commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} lvcreate --size {}G --name {}-lv1 myvg".format(clientIp,partSize,userName))
#print q

commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} mkfs.ext4 /dev/myvg/{}-lv1".format(clientIp,userName))
#print w

commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} mkdir -p /share/{}-lv1".format(clientIp,userName))
#print e

commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} mount /dev/myvg/{1}-lv1  /share/{1}-lv1".format(clientIp,userName))
#print r
	
commands.getstatusoutput("sshpass -p redhat scp {}:/etc/fstab /webcontent".format(clientIp))
#print t

commands.getstatusoutput("chown apache /webcontent/fstab")

fstabstring="/dev/myvg/{0}-lv1 /share/{0}-lv1 ext4 defaults 1 2".format(userName)
##never open /etc/fstab file in 'w' mode..system will corrupt
fstabfh=open('/webcontent/fstab','a')
fstabfh.write(fstabstring + "\n")
fstabfh.close()

commands.getstatusoutput("sshpass -p redhat scp /webcontent/fstab root@{}:/etc/fstab".format(clientIp))
#print y

commands.getstatusoutput("echo yes | rm /webcontent/fstab")

fstabStatus=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} mount -a".format(clientIp))

if fstabStatus[0]!=0:
	print "please check /etc/fstab file manually "
	exit()


commands.getstatusoutput("sshpass -p redhat sudo scp {}:/root/Desktop/project/exports /webcontent".format(clientIp))

commands.getstatusoutput("sudo chown apache /webcontent/exports")

shareLocator="/share/{0}-lv1 {1}".format(userName,clientIp)
##never open /etc/fstab file in 'w' mode..system will corrupt
nfsfh=open("/webcontent/exports",'a')
nfsfh.write(shareLocator + '\n')
nfsfh.close()	
print "dd" 

commands.getstatusoutput("sshpass -p redhat sudo scp /webcontent/exports root@{}:/root/Desktop/project/".format(clientIp))
print "bb"

commands.getstatusoutput("echo yes | sudo rm /webcontent/exports")


commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} systemctl restart nfs".format(clientIp))

	
