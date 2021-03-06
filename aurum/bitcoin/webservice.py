import urllib2


# Base class to hit any kind of REST url and get the response
class GetResponse(object):

	def __init__(self,url):
		self.url = url

	def submit(self):
		try:
			self.response = urllib2.urlopen(self.url).read()
		except (urllib2.URLError,urllib2.HTTPError),e:
			self.error = e 


# This class is used to get the response of getblockcount resource
class FetchBlockCount(GetResponse):

	def __init__(self):
		self.url = "http://blockchain.info/q/getblockcount"
		self.count = None  

	def submit(self):
		super(FetchBlockCount,self).submit()
		if self.response:
			self.count = int(self.response)


# Fetching the market data.
class FetchMarketData(GetResponse):

	def __init__(self):
		self.url = "http://api.bitcoincharts.com/v1/weighted_prices.json"
		self.market_data = None

	def submit(self):
		super(FetchMarketData,self).submit()
		if self.response:
			self.market_data = self.response


# Just for testing purpose.	
if __name__ == '__main__':
	obj = FetchBlockCount()	
	obj.submit()
	print obj.count 
	
	obj1 = FetchMarketData()
	obj1.submit()
	print obj1.market_data		
