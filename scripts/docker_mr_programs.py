#!/usr/bin/python2

import commands
import cgi
import cluster_files
import mrProgramsHtml

print "content-type: text/html"
print 


actionIp=cgi.FormContent()['actionIp'][0]

print """
<script>
function wc(fn,aip,outt){
	var s="Select";
	var n=s.localeCompare(fn);
	if (n==0)
	  alert("No file selected");
	else
	  document.location= 'docker_wc.py?actionIp=' + aip + '&fileName=' + fn + '&outDir=' + outt;
}

function anlyze(product,pay,reducer,aip,fn,outt){
	var s="Select";	
	var l=s.localeCompare(product);
	var p=s.localeCompare(pay);
	var t=s.localeCompare(reducer);
	var n=s.localeCompare(fn);
	if (n==0)
	  alert("No file selected for analysis");
		
	else if (outt=="")
	  alert("No output directory mentioned");

	else if (l==0)
	  alert("Select product");
	else if (p==0)
	  alert("Select payment mode");
	else if (t==0)	  
	  alert("Select Reducer type");
	else
	  document.location= 'mrPrograms.py?fileName=' + fn + '&outDir=' + outt + '&productType=' + product + '&payType=' + pay + '&reducerType=' + reducer + '&actionIp=' + aip;
}


</script>

"""

print """
<br />
<br />
<br />
<div align='center'>
<h2>Step 2 : MR programs</h2>
<br />
<br />
<table>
<tr>
	<td>Client Ip : </td>
	<td><input name='actionIp' value='{0}' readonly /></td>
</tr>
<tr>
	<td>Select file for analysis :</td>
	<td> 
""".format(actionIp)

cluster_files.fileNames(actionIp)

print """
</td>
</tr>
<tr>
	<td>Enter output directory :</td>
	<td><input id='outDir'   /></td>
</tr>
</table>
<br />
<br />
<input type='button' value='Preform WordCount job' onclick=wc(fileName.value,'{0}',outDir.value) />
<br />
<br />
or
<br />
<br />
""".format(actionIp)

print """
<h3>Filter data</h3>
<br />
<br />
<table>
<tr>
	<td>Select Product : </td>
	<td>
"""
mrProgramsHtml.productType()

print """
</td>
</tr>
<tr>
	<td>Select Payment mode : </td>
	<td>
"""
mrProgramsHtml.payType()

print """
</td>
</tr>
<tr>
	<td>Select action : </td>
	<td>
"""
mrProgramsHtml.reducerType()

print """
</td>
</tr>
</table>
<br />
<br />
<input type='submit' value='Analyze' onclick=anlyze(productType.value,payType.value,reducerType.value,'{0}',fileName.value,outDir.value) />
</div>
""".format(actionIp)


