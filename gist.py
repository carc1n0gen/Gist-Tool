#!/usr/bin/env python

from os import getenv
from os import environ
from sys import stdin
from optparse import OptionParser
from datetime import datetime
import time
import urllib2
import base64
import json

parser = OptionParser()
parser.add_option("-n", "--name", dest="filename", help="name of the gist")
parser.add_option("-d", "--description", dest="description", help="description of the gist")

(options, args) = parser.parse_args()

t = datetime.fromtimestamp(time.time())
timestamp = t.strftime("%Y-%m-%d %H:%M:%S")
description = timestamp
filename = "%s.txt" % timestamp
if options.description:
	description = options.description

if options.filename:
	filename = options.filename
	

API_URL=getenv("GH_API_URL") + "/gists"
API_USER=getenv("GH_USERNAME")
API_TOKEN=getenv("GH_GIST_TOKEN")
TEXT=""

for line in stdin:
	TEXT=TEXT + line

data = json.dumps({
	"description": description,
	"public": True,
	"files": {
		filename: {
			"content": TEXT
		}
	}
})

base64string = base64.b64encode("%s:%s" % (API_USER, API_TOKEN))
request = urllib2.Request(API_URL, data, headers={"Content-Type": "application/json", "Authorization": "Basic %s" % base64string})

try:
	f = urllib2.urlopen(request)
	response = json.loads(f.read())
	print response["html_url"]
except urllib2.URLError, e:
	print e
