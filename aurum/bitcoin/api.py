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
		excludes = ['created_at','id','timestamp']
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
			return False
		return datetime.now() - timedelta(**i_dict)


	# Currently handling the way to add filter interval for m,h,d 
	def get_object_list(self,request):
		u_filter = request.GET.get('interval',None) # Accessing 'interval' GET param from the request.
		results = super(MarketDataResource,self).get_object_list(request)
		date_obj = MarketDataResource.handle_interval(u_filter)
		if date_obj is None:
			output = results.order_by('-date_time')
		elif date_obj is False:
			output = MarketData.objects.none() # creating empty queryset when argument is invalid.
		else:
			output = results.filter(date_time__range=(date_obj,datetime.now()))
		return output.order_by('-date_time')

	@staticmethod
	def find_max_min(a_input):
		fields = ('highest_price','lowest_price','average_price')
		values = [list(),list(),list()]

		# Iterating the final data objects and storing the result 
		# of specified fields in another list to find max and min values.
		for d_json in a_input:
			for key,val in d_json.data.iteritems():
				try:
					pos = fields.index(key)
					values[pos].append(val)
				except ValueError,e:
					pass
			for k in fields:
				del d_json.data[k]


		# Iterating the list which has the values of specified fields
		# then find the max,min values 
		a_output = list()
		for v in values:
			if v:
				a_output.append(max(v))
			else:
				a_output.append(None)

		# Preparing the final output dictionary 	
		output = { k : v for k,v in zip(fields,a_output) }
		return output

	# overriding the method to remove unwanted fields in the response
	# also calling find_max_min to max,min values of specified fields.
	def alter_list_data_to_serialize(self, request, data):
		if 'meta' in data:
			del data['meta']
		values = MarketDataResource.find_max_min(data['objects'])
		data.update(values)
		return data 
