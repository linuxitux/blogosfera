#!/usr/bin/python
# Title      : alexa.py
# Description: Alexa Site Overview parser
# Author     : linuxitux
# Date       : 22-08-2016
# Usage      : ./alexa.py
# Notes      : Edit blogsf accordingly

import urllib2
import time
import operator
import datetime

# File containing domains, one per line
blogsf = "blogs.txt"

# Alexa Site Overview URL
url = "http://www.alexa.com/siteinfo/"

# Please, be gentle
sleeptime = 3

# Rank delimiters
substr1 = "<strong "
substr2 = "</strong"
substr3 = "-->"

# Get sites list (one per line)
with open(blogsf) as blogs:
	sites = blogs.readlines()

# Table to store ranks
results = []

for site in sites:
	# Get page
	req = urllib2.Request(url=url+site)
	p = urllib2.urlopen(req)
	resp = p.read()
	# Parse HTML response
	resp = resp[resp.index(substr1):]
	resp = resp[:resp.index(substr2)]
	resp = resp[resp.index(substr3)+3:]
	resp = resp.replace(" ","")
	rank = resp.replace("\n","")
	# Discard newline in site
	site = site.replace("\n","")
	# Discard commas in rank
	rank = rank.replace(",","")
	# Store (site,rank) pair in table
	row = (site,int(rank))
	results.append(row)
	time.sleep(sleeptime)

# Sort and print table in HTML format

# Print style

print """
<style>
.alexaranks {
font-family: monospace;
font-size: 13px;
color: #333;
}
a, a:active, a:focus, a:visited {
color: #2c9c30;
}
</style>
"""

# Print date
print '<p class="alexaranks"><i>Actualizado: '+datetime.date.today().strftime('%d/%m/%Y')+'</i></p>'

# Print table headers
print '<table id="alexaranks" class="alexaranks">'

# Counter
count = 1

# Print sorted rows (by rank)
for srow in sorted(results,key=lambda row: row[1]):
	site, rank = srow
	# Print line
	print '<tr><td>'+str(count)+'</td><td><a href="http://'+site+'/">'+site+'</a></td><td style="text-align: right;">'+"{:,}".format(rank)+'</td></tr>'
	count = count+1

# Print table closing tag
print '</table>'
print '<p> </p>'

# End
