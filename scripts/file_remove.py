#!/usr/bin/python2
import os
import commands
import cgi
import cluster_files

print "Content-Type: text/html"
print

actionIp=cgi.FormContent()['actionIp'][0]


print """
<script>
function rmv(fname,aip){
	var a="Select";
	var n=a.localeCompare(fname);
	if(n == 0)
	  alert("No file selected");
	else
	  document.location= 'file_remove_redirect.py?fileName=' + fname +'&actionIp=' + aip;
	  
}

</script>
"""


print """
<br />
<br />
<br />
<br />
<div align='center' >
<h2>File Remove</h2>

<h3><u>{0}</u></h3>
<br />
<br />
<br />
Select file : 
""".format(actionIp)

cluster_files.fileNames(actionIp)

print """
<br />
<br />
<input type='submit' onclick=rmv(fileName.value,'{}') />

<br />
<br />
<br />

<a href='../index.html' >Home</a> |
<a href='../file_upload.html'>File upload</a>
</div>
""".format(actionIp)
