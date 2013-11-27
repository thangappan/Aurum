# Using tastypie RESTful methods and classes
from tastypie.resources import Resource
from tastypie.cache import SimpleCache
from tastypie import fields

# our own webservice
from bitcoin.webservice import FetchBlockCount



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
