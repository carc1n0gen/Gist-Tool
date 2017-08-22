#!/usr/bin/env python

"""
Copyright (c) 2016 Carson Evans

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

--------------------------------------------------------------------------------

README

Three environment variables are required for this script to work

GH_API_URL:
	The url to the github api, example: https://api.github.com/v3.  Or your
	on-prem github, example: https://github.example.com/api/v3

GH_USERNAME:
	Your username on github or your on-prem github.

GH_GIST_TOKEN:
	A personal access token you generated on your account.  This token should
	have write access to gists.

This script reads input from stdin.  Easiest way to get the contents of a file
is to pipe from cat, example: cat some-text.txt | gist.py

You may provide a file name and/or description for the gist with 2 optional
parameters. These default the a timestamp.

-n, --name:
	The name of the gist

-d, --description
	The description of the gist

-p, --private
	A flag to indicate the gist should be private

"""

from os import getenv
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
parser.add_option("-p", "--private", action="store_true", dest="private", help="flag the gist as private")

(options, args) = parser.parse_args()

t = datetime.fromtimestamp(time.time())
timestamp = t.strftime("%Y-%m-%d %H:%M:%S")
description = timestamp
filename = "%s.txt" % timestamp
if options.description:
	description = options.description

if options.filename:
	filename = options.filename


API_ROOT=getenv("GH_API_URL")
API_USER=getenv("GH_USERNAME")
API_TOKEN=getenv("GH_GIST_TOKEN")

if not API_ROOT or not API_USER or not API_TOKEN:
	print "Required environment variables do not exist."
	print "See https://github.com/carc1n0gen/Gist-Tool for example configuration."
	exit(1)

API_URL=API_ROOT + "/gists"

TEXT=""

for line in stdin:
	TEXT=TEXT + line

data = json.dumps({
	"description": description,
	"public": options.private is not True,
	"files": {
		filename: {
			"content": TEXT
		}
	}
})

base64string = base64.b64encode("%s:%s" % (API_USER, API_TOKEN))
headers={
	"Content-Type": "application/json",
	"Authorization": "Basic %s" % base64string,
	"Accept": "application/vnd.github.v3+json"
}
request = urllib2.Request(API_URL, data, headers={"Content-Type": "application/json", "Authorization": "Basic %s" % base64string})

try:
	f = urllib2.urlopen(request)
	response = json.loads(f.read())
	print response["html_url"]
except urllib2.URLError, e:
	print e
