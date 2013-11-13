# Using tastypie RESTful methods and classes
from tastypie.resources import Resource,ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache
from tastypie import fields
from datetime import datetime,timedelta
from tastypie.serializers import Serializer

# our own webservice
from webservice import FetchBlockCount

from bitcoin.models import Currency,Exchange,MarketData


# Block count resource
class GetBlockCount(Resource):

	# Field to be populated in the API
	count = fields.IntegerField(attribute='count',null=True)
	error = fields.CharField(attribute='error',null=True)

	# defining meta fields 
	class Meta:
		resource_name = 'count'
		object_class = FetchBlockCount
		cache = SimpleCache(timeout=10)  # this is for 'caching'
		include_resource_uri = False
		excludes = ['error']
		print "Checking meta opetions"

	# --------------------------------------------------------------------------
	# -- Taken References from following link --
	# http://django-tastypie.readthedocs.org/en/latest/non_orm_data_sources.html
	# --------------------------------------------------------------------------

	# Following methods to be overriden to act like as a ORM object.
	def get_object_list(self,request):
		results = []
		newobj = FetchBlockCount()
		newobj.submit()
		results.append(newobj)
		return results
	
	def obj_get_list(self,request=None,**kwargs):
		return self.get_object_list(request)

	def obj_get(self,request=None,**kwargs):
		return self.get_object_list(request)[0]

# Exchange resource
class CurrencyResource(ModelResource):

	class Meta:
		queryset = Currency.objects.all()
		resource_name = 'currency'
		include_resource_uri = False
		excludes = ['created_at','c_id']
		cache = SimpleCache(timeout=10)  # this is for 'caching'
		filtering = {
			'name' : ['exact']
		}

# Exchange Resource
class ExchangeResource(ModelResource):
	
	class Meta:
		queryset = Exchange.objects.all()
		resource_name = 'exchange'
		include_resource_uri = False
		excludes = ['created_at','e_id','name']
		cache = SimpleCache(timeout=10)  # this is for 'caching'
		filtering = {
			'code' : ['exact']
		}


# Market Data Resource
class MarketDataResource(ModelResource):

	currency = fields.ForeignKey(CurrencyResource,'currency',full=True)
	exchange = fields.ForeignKey(ExchangeResource,'exchange',full=True)

	class Meta:

		queryset = MarketData.objects.all()
		excludes = ['created_at','id','timestamp','date_time']
		resource_name = 'market_data'
		include_resource_uri = False
		cache = SimpleCache(timeout=10)  # this is for 'caching'
		filtering = {
			'date_time' : ALL, 
			'currency' : ALL_WITH_RELATIONS,
			'exchange' : ALL_WITH_RELATIONS
		}

	 # Static method to handle common input for minutes,hours,days
	@staticmethod	
	def handle_interval(u_input):
		if not u_input:
			return None
	
		identifier = u_input[-1]
		number = u_input[:-1]
		i_dict = { 'hours' : 0, 'minutes' : 0, 'days' : 0 }
		i_map = { 'h' : 'hours', 'm' : 'minutes', 'd': 'days' }
		
		if identifier in i_map:
			i_dict[i_map[identifier]] = int(number)
		else:
			print "Please specify proper input ends with (d,m,h)"
			return None
		return datetime.now() - timedelta(**i_dict)


	# Currently handling the way to add filter interval for m,h,d 
	def get_object_list(self,request):
		u_filter = request.GET.get('interval',None) # Accessing 'interval' GET param from the request.
		results = super(MarketDataResource,self).get_object_list(request)
		date_obj = MarketDataResource.handle_interval(u_filter)
		if date_obj is None:
			output = results.order_by('-date_time')
		else:
			output = results.filter(date_time__range=(date_obj,datetime.now()))
		return output.order_by('-date_time')


	# overriding the method to remove unwanted fields in the response
	def alter_list_data_to_serialize(self, request, data):
		if 'meta' in data:
			del data['meta']
		return data
