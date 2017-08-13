#!/usr/bin/python2

import cgi
import docker_images_list

print "content-type: text/html"
print


actionIp=cgi.FormContent()['actionIp'][0]

print """
<br />
<br />
<br />
<div align='center'>
<h2>Launch new container</h2>
<br />
<br />
<form action='docker_home_redirect.py'>
<table>
  <tr>
	<td>Enter IP : </td>
	<td><input readonly value="{0}" placeholder="{0}" name='actionIp' /></td>
  </tr>

  <tr>
	<td>Select image :</td>
	<td>
  
""".format(actionIp)

docker_images_list.docker_list(actionIp)


print """
	</td>
  </tr>

  <tr>
	<td>Enter container name: </td>
	<td><input name='cName' /><br /></td>
  </tr>


</table>
<br />
<br />
<br />
<input type='submit' value='Launch' />
</form>
<br />
<br />
<br />
<a href='../docker_home.html'>Change IP</a>
</div>
"""
