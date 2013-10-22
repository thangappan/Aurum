from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from bitcoin.api import GetBlockCount
from tastypie.api import Api

api = Api()
api.register(GetBlockCount())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aurum.views.home', name='home'),
    # url(r'^aurum/', include('aurum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

	# REST API
	(r'api/',include(api.urls)),
)
