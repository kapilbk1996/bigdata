#!/usr/bin/python2


import commands
import cgi
import re

print "content-type: text/html"
print 

actionIp=cgi.FormContent()['actionIp'][0]
cName=cgi.FormContent()['cname'][0]

#for id
doc_idd=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].Id'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_id=doc_idd[1].split("\n")[-1]
else:
	doc_id=doc_idd[1][1:-1]
#for created
doc_c=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].Created'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_created=doc_c[1].split("\n")[-1]
else:
	doc_created=doc_c[1][1:-1]

#for status
doc_s=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].State.Status'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_status=doc_s[1].split(".")[-1]
else:
	doc_status=doc_s[1][1:-1]

#for pid
doc_p=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].State.Pid'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_pid=doc_p[1].split(".")[-1]
else:
	doc_pid=doc_p[1][1:-1]

#for image
doc_i=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].Image'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_image=doc_i[1].split("\n")[-1]
else:
	doc_image=doc_i[1][1:-1]

#for network mode
doc_nm=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].HostConfig.NetworkMode'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_netmode=doc_nm[1].split("\n")[-1]
else:
	doc_netmode=doc_nm[1][1:-1]

#for Auto remove
doc_ar=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].HostConfig.AutoRemove'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_autormv=doc_ar[1].split("\n")[-1]
else:
	doc_autormv=doc_ar[1][1:-1]

#for group add
doc_ga=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].HostConfig.GroupAdd'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_groupadd=doc_ga[1].split("\n")[-1]
else:
	doc_groupadd=doc_ga[1][1:-1]

#for privilage
doc_pv=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].HostConfig.Privileged'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_privileged=doc_pv[1].split("\n")[-1]
else:
	doc_privileged=doc_pv[1][1:-1]

#for ip addresss
doc_ipp=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].NetworkSettings.IPAddress'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_ip=doc_ipp[1].split("\n")[-1]
else:
	doc_ip=doc_ipp[1][1:-1]

#for gateway
doc_gw=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].NetworkSettings.Gateway'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_gateway=doc_gw[1].split("\n")[-1]
else:
	doc_gateway=doc_gw[1][1:-1]

#for mac address
doc_m=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].NetworkSettings.MacAddress'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_mac=doc_m[1].split("\n")[-1]
else:
	doc_mac=doc_m[1][1:-1]

#for subnet
doc_pp=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].NetworkSettings.IPPrefixLen'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_subnet=doc_pp[1].split("\n")[-1]
else:
	doc_subnet=doc_pp[1][1:-1]

#for network id
doc_nid=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].NetworkSettings.Networks.bridge.NetworkID'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_netid=doc_nid[1].split("\n")[-1]
else:
	doc_netid=doc_nid[1][1:-1]

#for ports
doc_po=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].NetworkSettings.Ports'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_ports=doc_po[1].split("\r")[-1]
else:
	doc_ports=doc_po[1][1:-1]

#for bridge
doc_br=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].NetworkSettings.Bridge'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_bridge=doc_br[1].split("\n")[-1]
else:
	doc_bridge=doc_br[1][1:-1]

#for image name
doc_ii=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].Config.Image'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_imgname=doc_ii[1].split("\n")[-1]
else:
	doc_imgname=doc_ii[1][1:-1]

#for host name
doc_hn=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].Config.Hostname'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_hostname=doc_hn[1].split("\n")[-1]
else:
	doc_hostname=doc_hn[1][1:-1]

#for mounts
doc_hn=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].Mounts'".format(cName,actionIp))
if re.search("Warning: Permanently",doc_idd[1]):
	doc_mounts=doc_hn[1].split("\r")[-1]
else:
	doc_mounts=doc_hn[1][1:-1]


print """
<!DOCTYPE html>
<html>
<head>
<style>
th,td {
  padding-left:50px;
  padding-bottom:15px;
}
</style>
"""

print """
<title>{0}-{1}</title>
</head>
<body>
<br />
<br />
<br />
<div align='center' >
 <h2>Container : {0} - {1}</h2>

<br />
<br />
<br />
""".format(cName,actionIp)

print"""
<u><h3 >Basic Details</h3></u>
<br />
<br />
<table width='500' height='450' >
<tr>
	<td>Name</td>
	<td>{19}</td>
</tr>

<tr>
	<td>Id</td>
	<td>{0}</td>
</tr>

<tr>
	<td>Created</td>
	<td>{1}</td>
</tr>

<tr>
	<td>Status</td>
	<td>{2}</td>
</tr>

<tr>
	<td>Pid</td>
	<td>{3}</td>
</tr>

<tr>
	<td>Image Name</td>
	<td>{16}</td>
</tr>

<tr>
	<td>Image ID</td>
	<td>{4}</td>
</tr>

<tr>
	<td>Network Mode</td>
	<td>{5}</td>
</tr>

<tr>
	<td>Auto Remove</td>
	<td>{6}</td>
</tr>

<tr>
	<td>Group add</td>
	<td>{7}</td>
</tr>

<tr>
	<td>Privileged</td>
	<td>{8}</td>
</tr>

<tr>
	<td>Host Name</td>
	<td>{17}</td>
</tr>

<tr>
	<td>Mounts</td>
	<td>{18}</td>
</tr>

</table>

<br />
<br />
<u><h3 >Network Details</h3></u>
<br />
<br />
<table >
<tr>
	<td>Ip address</td>
	<td>{9}</td>
</tr>
<tr>
	<td>Gateway</td>
	<td>{10}</td>
</tr>
<tr>
	<td>MAC address</td>
	<td>{11}</td>
</tr>
<tr>
	<td>IPPrefixLen</td>
	<td>{12}</td>
</tr>
<tr>
	<td>Network ID</td>
	<td>{13}</td>
</tr>
<tr>
	<td>Ports</td>
	<td>{14}</td>
</tr>
<tr>
	<td>Bridge</td>
	<td>{15}</td>
</tr>
</table>
</div>
<br />
<br />
<br />
</body>
</html>
""".format(doc_id[1:-1],doc_created[1:-1],doc_status,doc_pid,doc_image[1:-1],doc_netmode[1:-1],doc_autormv,doc_groupadd,doc_privileged,doc_ip[1:-1],doc_gateway[1:-1],doc_mac[1:-1],doc_subnet,doc_netid[1:-1],doc_ports,doc_bridge,doc_imgname[1:-1],doc_hostname[1:-1],doc_mounts,cName)


