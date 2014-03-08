from django.conf.urls import patterns, include, url

from purchase.views import *

urlpatterns = patterns('',
	url(r'^purchase-entry/$', PurchaseEntry.as_view(),name='purchase'),

)