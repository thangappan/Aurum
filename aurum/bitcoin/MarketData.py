#!/usr/bin/env python

import sys,os
import json,urllib2
import datetime

# making our application to sys.path
# If this script configured in cron-job then need to configure PYTHONPATH appropriately. 
# Need to choose either way sys.path or PYTHONPATH env
sys.path.append('../')

# Enabling settings page to get database params
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aurum.settings")

from bitcoin.models import Currency,Exchange,MarketData

# getting the currencies and exchanges.
db_currencies = Currency.objects.all()
db_exchanges  = Exchange.objects.all()


# Getting exchange API links from configuration file.
# Currently hardcoding the path in the script itself.
# Here the currency key for every exchange will decide
# whether the url have to be modified or not.
EXCHANGE_LINKS = {
	'mtgox' : { 
				'url' : 'https://data.mtgox.com/api/2/BTC{0}/money/ticker',
				'currency': 'FORMATTER'
			  },
}


# Hitting the link and getting the repsonse 
def fetch_repsonse(url):
	try:
		print url
		repsonse = urllib2.urlopen(url)
		content = json.loads(repsonse.read())
	except (urllib2.HTTPError,urllib2.URLError) as e:
		print e
		sys.exit(-1)
	return content


# Converting timestamp to datetime object.
def convert_to_local(epoch):
	epoch = int(epoch)
	local_time = float('{0}.{1}'.format( int( epoch / 1000000 ), int( epoch % 1000000 ) ) )
	return datetime.datetime.fromtimestamp(local_time)


# Function to fetch market data 
def obtain_market_data(link):

	data = fetch_repsonse(link)
	if not data:
		print "Coudln't get the market data for given url %s" % (link,)
		return False
	
	if data.get('result') != 'success':
		print "Market data API %s Failed" % (link,)
		return False

	# The way of getting market data might be different for all the exchanges
	# TODO need to find a common way
	output = data.get('data')
	timestamp = output.get('now')
	date_time = convert_to_local(timestamp)
	high = output.get('high').get('value')
	low  = output.get('low').get('value')
	avg  = output.get('avg').get('value')
	print timestamp,high,low,date_time,avg
	return { 'timestamp' : str(timestamp), 'highest_price' : float(high), \
			 'lowest_price' : float(low) , 'average_price' : float(avg), \
			  'date_time' : date_time }
		

# For each currency configured in the database will be updated for each
# configured exchanges. Make sure that exchange configured in database should be 
# configured to EXCHANGE_LINKS variable.
for c_obj in db_currencies:

	currency = c_obj.name
	for e_obj in db_exchanges: 
		e_code = e_obj.code
		e_name = e_obj.name
		if e_code.lower() not in EXCHANGE_LINKS:
			continue  # skipping when no link for exchange code.
		e_details = EXCHANGE_LINKS[e_code.lower()]


		# Getting the url to be used to obtain market data
		url_link = e_details['url']
		if e_details['currency'] == 'FORMATTER':
			url_link = e_details['url'].format(currency)

		# Getting the details and storing into database.
		print currency, e_code, url_link
		market_data = obtain_market_data(url_link)
		if market_data:
			m_obj = MarketData(currency=c_obj,exchange=e_obj,**market_data)
			m_obj.save()
