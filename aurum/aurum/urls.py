from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from bitcoin.api import GetBlockCount,MarketDataResource,NewsResource
from tastypie.api import Api

api = Api(api_name="aurum")
api.register(GetBlockCount())
api.register(MarketDataResource())
api.register(NewsResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aurum.views.home', name='home'),
    # url(r'^aurum/', include('aurum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

	# REST API
	(r'',include(api.urls)),
)
