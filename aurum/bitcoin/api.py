# Using tastypie RESTful methods and classes
from tastypie.resources import Resource,ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache
from tastypie import fields
from datetime import datetime,timedelta

# our own webservice
from webservice import FetchBlockCount ,FetchMarketData

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


class CurrencyResource(ModelResource):

	class Meta:
		queryset = Currency.objects.all()
		resource_name = 'currency'
		excludes = ['created_at','c_id']
		filtering = {
			'name' : ['exact']
		}


class ExchangeResource(ModelResource):
	
	class Meta:
		queryset = Exchange.objects.all()
		resource_name = 'exchange'
		excludes = ['created_at','e_id']
		filtering = {
			'code' : ['exact']
		}


# Market Data Resource
class MarketDataResource(ModelResource):

	currency = fields.ForeignKey(CurrencyResource,'currency',full=True)
	exchange = fields.ForeignKey(ExchangeResource,'exchange',full=True)

	class Meta:

		#queryset = MarketData.objects.filter(date_time__range=(datetime.now() - timedelta(minutes=5), datetime.now()))
		queryset = MarketData.objects.all()
		excludes = ['created_at','id','timestamp','date_time']
		resource_name = 'market_data'
		filtering = {
			'date_time' : ALL, 
			'currency' : ALL_WITH_RELATIONS,
			'exchange' : ALL_WITH_RELATIONS
		}

	# Currently handling the way to add filters for 5m,1h,7d,
	def get_object_list(self,request):
		filter = request.GET.get('interval',None) # Accessing 'interval' GET param from the request.
		results = super(MarketDataResource,self).get_object_list(request)
		if filter == '5m':
			output = results.filter(date_time__range=(datetime.now() - timedelta(minutes=5),datetime.now())).order_by('-date_time')
		elif filter == '1h':
			output = results.filter(date_time__range=(datetime.now() - timedelta(hours=1),datetime.now())).order_by('-date_time')
		elif filter == '7d':
			output = results.filter(date_time__range=(datetime.now() - timedelta(days=7),datetime.now())).order_by('-date_time')
		elif filter == '30d':
			output = results.filter(date_time__range=(datetime.now() - timedelta(days=30),datetime.now())).order_by('-date_time')
		else:
			output = results.order_by('-date_time')
		return output	
