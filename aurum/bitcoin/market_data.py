#!/usr/bin/env python

import json
import urllib2
import sys
import time

def fetch_repsonse(url):

	try:
		print url
		repsonse = urllib2.urlopen(url)
		content = json.loads(repsonse.read())
	except (urllib2.HTTPError,urllib2.URLError) as e:
		print e
		sys.exit(-1)
	return content


def form_url(currency_name):
	
	base_url_formatter = 'https://data.mtgox.com/api/2/BTC{0}/money/ticker'
	return base_url_formatter.format(currency_name)


def convert_to_local(epoch):

	epoch = int(epoch)
	local_time = float('{0}.{1}'.format( int( epoch / 1000000 ), int( epoch % 1000000 ) ) )
	return time.strftime('%d-%m-%Y %H:%M:%S',time.localtime(local_time))


def obtain_market_data(currency_name):

	data = fetch_repsonse(form_url(currency_name))
	if not data:
		print "Coudln't get the data"
		return False
	
	if data.get('result') != 'success':
		print "API Failed"
		return False

	output = data.get('data')
	timestamp = output.get('now')
	date_time = convert_to_local(timestamp)
	high = output.get('high').get('value')
	low  = output.get('low').get('value')
	buy  = output.get('buy').get('value')
	sell = output.get('sell').get('value')
	last_local = output.get('last_local').get('value')
	print timestamp,high,low,buy,sell,last_local,date_time,timestamp


if __name__ == '__main__':
	obtain_market_data('USD')
