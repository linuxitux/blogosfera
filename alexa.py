# Alexa Site Overview parser

import urllib2
import time
import operator

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

# Print table headers
print '<table id="alexaranks" class="alexaranks">'

# Print sorted rows (by rank)
for srow in sorted(results,key=lambda row: row[1]):
	site, rank = srow
	# Print line
	print '<tr><td><a href="http://'+site+'/">'+site+'</a></td><td>'+"{:,}".format(rank)+'</td></tr>'

# Print table closing tag
print '</table>'

# End
