

import urllib2

class GetResponse(object):

	def __init__(self,url=None):
		if url is not None:
			self.submit(url)
	
	def submit(self,url):
		try:
			self.response = urllib2.urlopen(url).read()
		except (URLError,HTTPError),e:
			self.response = { "error" : e }
	

#robj = GetResponse()
#robj.submit("http://blockchain.info/q/getblockcount")
#print robj.response
		
robj = GetResponse("https://blockchain.info/q/getblockcount")
print robj.response
			
			
		

