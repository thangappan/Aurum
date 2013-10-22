import urllib2


# Main class to hit any kind of REST url and get the response
class GetResponse(object):

	def __init__(self,url=None):
		if url is not None:
			self.submit(url)
	
	def submit(self,url):
		try:
			self.response = urllib2.urlopen(url).read()
		except (urllib2.URLError,urllib2.HTTPError),e:
			self.response = { "error" : e }


# This class is used to get the response of getblockcount resource
class FetchBlockCount(object):

	def __init__(self,initial=None):
		url = "http://blockchain.info/q/getblockcount"
		self.count = None; self.error = None
		self.get_count(url)

	def get_count(self,url):
		web_obj = GetResponse(url)
		data = web_obj.response
		if data and type(data) != type({}):
			self.count = int(data)
		else:
			self.error = data.get('error')


# Just for testing purpose.	
if __name__ == '__main__':	
	robj = GetResponse("https://blockchain.info/q/getblockcount")
	print robj.response
