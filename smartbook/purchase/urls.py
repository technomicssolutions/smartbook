from django.conf.urls import patterns, include, url

from purchase.views import *

urlpatterns = patterns('',
	url(r'^$', PurchaseDetail.as_view(), name='purchase_details'),
	url(r'^entry/$', PurchaseEntry.as_view(),name='purchase'),
	url(r'^edit/$', PurchaseEdit.as_view(),name='edit_purchase'),
)