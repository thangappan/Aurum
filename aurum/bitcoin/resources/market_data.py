# Using tastypie RESTful methods and classes
from tastypie.resources import Resource,ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache
from tastypie import fields
from bitcoin.models import Currency,Exchange,MarketData
from datetime import datetime,timedelta

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

	def check_filtering(self, field_name, filter_type='exact', filter_bits=None):
		u_filters_map = { 'currency' : u'name', 'exchange' : u'code' }
		if field_name in u_filters_map and not filter_bits:
			filter_bits.append(u_filters_map[field_name])
			self.u_filters.append(field_name)
		return super(MarketDataResource,self).check_filtering(field_name, filter_type,filter_bits)

	def apply_filters(self,request,applicable_filters):
		return super(MarketDataResource,self).apply_filters(request,applicable_filters)

	def build_filters(self,filters=None):
		self.u_filters = list()
		orm_filters = super(MarketDataResource,self).build_filters(filters)
		return orm_filters

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

	def dehydrate_currency(self,bundle):
		bundle.data['currency'] = bundle.data['currency'].data['name']
		return bundle.data['currency']

	def dehydrate_exchange(self,bundle):
		bundle.data['exchange'] = bundle.data['exchange'].data['code']
		return bundle.data['exchange']

	def make_it_common(self,data):
		common = dict()
		print "user filtetrs",self.u_filters
		for d_json in data['objects']:
			for field in self.u_filters:
				if field in d_json.data:
					common[field] = d_json.data[field]
					d_json.data.pop(field)
		if common:
			data.update(common)
		return data 

	# overriding the method to remove unwanted fields in the response
	# also calling find_max_min to max,min values of specified fields.
	def alter_list_data_to_serialize(self, request, data):
		if 'meta' in data:
			del data['meta']
		values = MarketDataResource.find_max_min(data['objects'])
		data.update(values)
		data = self.make_it_common(data)
		return data 
