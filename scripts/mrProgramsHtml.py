#!/usr/bin/python2

import commands
import cgi


def productType():
	print """
<select id='productType'>
<option>Select</option>
<option>Product1</option>
<option>Product2</option>
<option>Product3</option>
<option>None</option>
</select>
"""

def payType():
	print """
<select id='payType'>
<option>Select</option>
<option>Mastercard</option>
<option>Visa</option>
<option>Diners</option>
<option>Amex</option>
</select>
"""

def reducerType():
	print """
<select id='reducerType'>
<option>Select</option>
<option>Count</option>
<option>view</option>
</select>
"""
