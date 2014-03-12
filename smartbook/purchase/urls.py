from django.conf.urls import patterns, include, url

from purchase.views import *

urlpatterns = patterns('',
	url(r'^$', PurchaseDetail.as_view(), name='purchase_details'),
	url(r'^entry/$', PurchaseEntry.as_view(),name='purchase'),
	url(r'^edit/$', PurchaseEdit.as_view(),name='edit_purchase'),
	url(r'^vendor_account/list/$', VendorAccountList.as_view(),name='vendor_accounts'),
	url(r'^vendor_account/(?P<vendor>\w+)/$', VendorAccountDetails.as_view(),name='vendor_account_details'),
)