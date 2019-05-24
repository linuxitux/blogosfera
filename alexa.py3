#!/usr/bin/python
# Title      : alexa.py
# Description: Alexa Site Overview parser
# Author     : linuxitux
# Date       : 22-08-2016
# Usage      : ./alexa.py
# Notes      : Edit blogsf accordingly

import urllib.request, urllib.error, urllib.parse
import sys
import time
import operator
import datetime

# File containing domains, one per line
blogsf = "~/blogs.txt"

# Alexa Site Overview URL
url = "http://www.alexa.com/siteinfo/"

# Please, be gentle
sleeptime = 3

# Rank delimiters
substr1 = '<p class="big data">'
substr2 = "</p"
substr3 = "</span>"

# Get current date
date = time.strftime("%Y-%m-%d")

# Database <--- facepalm
outfile = open("~/ranks_"+date, "w")

# Get sites list (one per line)
with open(blogsf) as blogs:
  sites = blogs.readlines()

# Table to store ranks
results = []

for site in sites:
  # Get page
  req = urllib.request.Request(url=url+site)
  p = urllib.request.urlopen(req)
  resp = str(p.read())
  # Parse HTML response
  try:
    resp = resp[resp.index(substr1):]
    resp = resp[:resp.index(substr2)]
    resp = resp[resp.index(substr3)+len(substr3):]
    resp = resp.replace(" ","").rstrip("\\n\\t")
  except ValueError:
    # When Alexa doesn't have enough data to output a ranking score
    resp = '0'

  rank = resp
  # Discard newline in site
  site = site.replace("\n","")
  # Discard commas in rank
  rank = rank.replace(",","")
  # Store (site,rank) pair in table
  try:
    row = (site,int(rank))
    results.append(row)
  except Exception:
    print(site+" has no rank", file=sys.stderr)
    row = (site,0)
    results.append(row)
  time.sleep(sleeptime)

# Sort and print table in HTML format

# Print style

print("""
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
""")

# Print date
print('<p class="alexaranks"><i>Actualizado: '+datetime.date.today().strftime('%d/%m/%Y')+'</i></p>')

# Print table headers
print('<table id="alexaranks" class="alexaranks">')

# Counter
count = 1

# Print sorted rows (by rank)
for srow in sorted(results,key=lambda row: row[1]):
  site, rank = srow
  # Print line, if rank not zero
  if rank > 0:
    print('<tr><td>'+str(count)+'</td><td><a href="http://'+site+'/">'+site+'</a></td><td style="text-align: right;">'+"{:,}".format(rank)+'</td></tr>')
    outfile.write(site+","+str(rank)+"\n")
    count = count+1

# Print table closing tag
print('</table>')
print('<p> </p>')

# "Disconnect" from "database"
outfile.close()

# End

