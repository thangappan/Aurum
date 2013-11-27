# Using tastypie RESTful methods and classes
from tastypie.resources import Resource,ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.cache import SimpleCache
from tastypie.authorization import Authorization
from tastypie import fields

# News model from bitcoin
from bitcoin.models import NewsModel


class NewsResource(ModelResource):


	class Meta:
		queryset = NewsModel.objects.all()
		resource_name = 'news'
		include_resource_uri = False
		excludes = ['created_at','updated_at']
		cache = SimpleCache(timeout=10)

		# To avoid HTTP/1.0 401 UNAUTHORIZED 
		authorization= Authorization()

		# To avoid HTTP/1.0 204 NO CONTENT
		always_return_data = True

	#--------------------------------------------------------
	# Hydration Cycle - From Userinput to Data model
	# Just getting the value from DB and saving the DB model by adding it.
	#--------------------------------------------------------
	def hydrate_shared_count(self,bundle):
		count = NewsModel.objects.get(pk=bundle.obj.pk).shared_count
		bundle.data['shared_count'] += int(count)
		return bundle

	def hydrate_read_count(self,bundle):
		count = NewsModel.objects.get(pk=bundle.obj.pk).read_count
		bundle.data['read_count'] += int(count)
		return bundle

	# Making the ORM wise ordering happen by overriding the following method
	# shared - shared_count and read - read_count
	def get_object_list(self,request):
		f_shared = request.GET.get('order',None) # Accessing 'order_shared' GET param from the request.
		results = super(NewsResource,self).get_object_list(request)
		if f_shared == 'shared':
			results = results.order_by('-shared_count')
		elif f_shared == 'read':
			results = results.order_by('-read_count')
		return results

	#--------------------------------------------------------
	# Dehydration Cycle = From data model to JSON input 
	#--------------------------------------------------------
	# overriding the method to remove unwanted fields in the response
	def alter_list_data_to_serialize(self, request, data):
		if 'meta' in data:
			del data['meta']

		if 'objects' in data:
			c_data = data['objects']
			del data['objects']
			data['news'] = c_data
		return data 
