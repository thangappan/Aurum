#!/usr/bin/env python

import feedparser
import sys,os
import time
from dateutil import parser

url = "http://news.google.co.in/news?q=bitcoin&output=rss"

class GoogleNewsFeed(object):

	def __init__(self,pattern):
		self.url = "http://news.google.co.in/news?q={0}&output=rss".format(pattern) 
		self.feed = feedparser.parse(self.url)
		self.__dict__.update(self.feed)

	def __del__(self):
		del self.url
		del self.feed

result = GoogleNewsFeed('bitcoin')

if result.bozo == 1:
	print "Failed to get the news with the exception {0}".format(result.bozo_exception)
	sys.exit(-1)
	
required_entry_fields = ('title','link','published')
db_fields = ('name','link','pub_date')

# making our application to sys.path
# If this script configured in cron-job then need to configure PYTHONPATH appropriately. 
# Need to choose either way sys.path or PYTHONPATH env
sys.path.append('../../')

# Enabling settings page to get database params
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aurum.settings")

from bitcoin.models import NewsModel

for val in result.entries:

	params = dict()
	for field in val.keys():
		try:
			ind = required_entry_fields.index(field)		
			detail = val[required_entry_fields[ind]]
			if field == 'published':
				detail = parser.parse(detail)
			print detail
			params.update({db_fields[ind] : detail})
		except ValueError,e:
			pass
	print 
	if params:
		c = NewsModel(**params)
		c.save()
