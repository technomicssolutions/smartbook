from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from purchase.views import *

urlpatterns = patterns('',
	url(r'^$', login_required(PurchaseDetail.as_view()), name='purchase_details'),
	url(r'^entry/$', login_required(PurchaseEntry.as_view()), name='purchase'),
	url(r'^edit/$', login_required(PurchaseEdit.as_view()), name='edit_purchase'),
	url(r'^return/$', login_required(PurchaseReturnView.as_view()), name='purchase_return'),
	url(r'^return_edit/$', login_required(PurchaseReturnEdit.as_view()), name='edit_purchase_return'),
	url(r'^vendor_accounts/$', login_required(VendorAccounts.as_view()), name='vendor_accounts'),
	url(r'^vendor_account/$', login_required(VendorAccountDetails.as_view()), name='vendor_account_details'),
)