#!/usr/bin/python2


import commands
import cgi
import re

print "content-type: text/html"



actionIp=cgi.FormContent()['actionIp'][0]
print "set-cookie: actionIp={}".format(actionIp)
print


print """
<script>
function removee(mycname,actionIp)
{
	document.location='docker_remove.py?x=' + mycname + '&actionIp=' + actionIp;
}
function removeAll(mycname,actionIp)
{
	r=confirm("Do you want to remove all containers ??");
	if (r == true) {    
	document.location='docker_remove.py?x=' + mycname + '&actionIp=' + actionIp;
}
}
function lw(action,actionIp,mycname)
{
if (action=="Start"){
	document.location='docker_start.py?x=' + mycname + '&actionIp=' + actionIp;
}
else{
	document.location='docker_stop.py?x=' + mycname + '&actionIp=' + actionIp;
}
}

</script>
<br />
<br />
<br />

<div align='center'>
"""


print "<table border='5' >"
print "<tr><th>Image Name</th><th>ContainerName</th><th>Status</th><th>IP address</th><th>Action</th><th>Remove</th><th>More Detail</th></tr>"

print "<h2>Docker Dashboard - {}</h2>".format(actionIp)
flag=0
for i in commands.getoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {} docker ps -a".format(actionIp)).split('\n'):
	
	
	if re.search("Failed to add",i) or re.search("CONTAINER[ ]ID",i) or re.search("Could not create directory",i):	
		pass

	else:
		flag=1
		j=i.split()
		ccStatus=commands.getoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -o 'UserKnownHostsFile=/dev/null'  -l root {1} docker inspect {0} | jq '.[].State.Status'".format(j[-1],actionIp))
		cStatuss=ccStatus.split(".")
		cStatus=cStatuss[-1]
		
		if re.search("running",cStatus):
		  temp="Stop"
		else:
		  temp="Start"
		
		myip=commands.getstatusoutput("sshpass -p redhat ssh -o stricthostkeychecking=no -l root {0} docker inspect {1} | jq '.[].NetworkSettings.Networks.bridge.IPAddress'".format(actionIp,j[-1]))
		myipp=myip[1].split("\n")[-1]
		
		temp_input="asdfghjkl456321asdf"
			
		print "<tr><td>" + j[1] + "</td><td>" + j[-1] + "</td><td>" + cStatus[2:-1] +  "</td><td>" + myipp[1:-1] +"</td><td> <input id='" + temp + "' type='button' value='" + temp + "' onclick=lw(this.id,'" + actionIp + "','" + j[-1] +"') />   </td><td>  <input id='" + j[-1]    +  "' type='button' value='Remove' onclick=removee(this.id,'" + actionIp + "')  /> </td><td><a href='docker_detail.py?actionIp="+ actionIp +"&cname="+j[-1] +" ' target='_blank' >Click here</a></td> </tr>"

if flag==0:
	print "<h2>No container to display</h2>"


s="""
</table>
<br /><br />
<a href='../docker_home.html'>launch new container</a> |
<a href='../index.html'>Home</a> | 
<a href='docker_online_shell.py?actionIp={0} ' target='_blank'>Get online shell</a><br />
<br />
<br />
<br />
<input type='button' onclick=removeAll('allall','{0}') value='Remove all containers' />

</div>
<div align='right'>



</div>
""".format(actionIp,"")

print s











