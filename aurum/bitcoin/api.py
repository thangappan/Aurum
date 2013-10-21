from tastypie.resources import ModelResource,Resource
from tastypie.cache import SimpleCache
from bitcoin.models import Count
from webservice import  GetResponse


class GetBlockCount(ModelResource):
	
	class Meta:
		resource_name = 'count'
		queryset = Count.objects.all()
		excludes = ['id']
		cache = SimpleCache(timeout=10)


class FetchBlockCount(object):

	def __init__(self):
		self.url = "http://blockchain.info/q/getblockcount"

	def get_count(self):
		data = GetResponse(self.url)
		if data and type(data) != type({}):
			data = { 'count' : data }
		return data 
			

class BlockCount(Resource):

	class Meta:
		resource_name = 'block_count'
		object_class = FetchBlockCount

	def obj_get_list(self,request=None,**kwargs):
		obj = FetchBlockCount()
		response = obj.get_count()
		return [obj]
