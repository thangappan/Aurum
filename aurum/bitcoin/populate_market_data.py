#!/usr/bin/env python

import sys,os
import json,telnetlib
import datetime


# making our application to sys.path
# If this script configured in cron-job then need to configure PYTHONPATH appropriately. 
# Need to choose either way sys.path or PYTHONPATH env
sys.path.append('../../')

# Enabling settings page to get database params
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aurum.settings")

from bitcoin.models import Currency,Exchange,MarketData
from django.utils import timezone
from django.db.utils import IntegrityError


# Connecting to telnet session and getting the response.
def fetch_repsonse(host='api.bitcoincharts.com',port=27007):
	content = ''
	#while content:
	#	try:
	#		print url
	#		telnet_obj = telnetlib.Telnet(host,port)
	#		content = telnet_obj.read_very_lazy()
	#	except EOFError,e
	#		print e
	content = '{"volume": 0.0102555, "timestamp": 1387366213, "price": 1400.0, "symbol": "bitcurexPLN", "id": 113393147}\n{"volume": 0.07, "timestamp": 1387366191, "price": 2113, "symbol": "btcnCNY", "id": 113393335}\n{"volume": 0.2, "timestamp": 1387366169, "price": 440.0, "symbol": "bitstampUSD", "id": 113392793}\n{"volume": 0.00999998, "timestamp": 1387366167, "price": 351.56957, "symbol": "mtgoxEUR", "id": 113392759}'
	return content
	

# Converting timestamp to datetime object.
def convert_to_local(epoch):
	epoch = int(epoch)
	return datetime.datetime.fromtimestamp(epoch).replace(tzinfo=timezone.utc)


def update_exchange_currency(symbol):

	if not symbol:
		return (False,None)

	exchange = symbol[:-3]
	currency = symbol[-3:]

	e_object, e_created = Exchange.objects.get_or_create(code=symbol,name=exchange)
	if e_created:
		print "New Exchange Created named {0}".format(exchange)

	c_object, c_created = Currency.objects.get_or_create(name=currency)
	if c_created:
		print "New Currency Created named {0}".format(currency)
	
	return (e_object,c_object)


def update_opening_or_closing_price(c_obj):

	l_obj = MarketData.objects.latest('created_at')
	if l_obj.date_time


# Function to fetch market data and populate into database.
def obtain_and_store_marekt_data():


	# Gettig repsonse from telnet session 	
	response = fetch_repsonse()
	if not response:
		print "No such data at this time in the stream"
		return False

	# Spliting data and loads as JSON response
	for data in response.split("\n"):
		data = json.loads(data)
		volume = data.get('volume')
		price  = data.get('price')
		timestamp = data.get('timestamp')
		symbol = data.get('symbol')
		t_id = data.get('id')
		
		date_time = convert_to_local(timestamp)
		print volume,price,timestamp,symbol,t_id,date_time

		(e_object,c_object) = update_exchange_currency(symbol)
		if e_object is False:
			continue # Not exiting. Just skipping the current entry
		
		market_data = { 
		  'trans_id' : str(t_id), 
		  'price'    : float(price),
		  'volume'   : float(volume),
		  'timestamp': str(timestamp),
		  'date_time': date_time
		}

		try:
			m_obj = MarketData(currency=c_object,exchange=e_object,**market_data)
			m_obj.save()
		except IntegrityError,e:
			print "Already data exist: ",t_id

# TODO: This has to be modified in loop with daemon
obtain_and_store_marekt_data()
