from django.conf.urls import patterns, include, url

from sales.views import *

urlpatterns = patterns('',
#	url(r'^$', Home.as_view(), name='home'),


	url(r'^entry/$', SalesEntry.as_view(), name='sales'),
	#url(r'sales_entry/$', SalesEntry.as_view(), name='sales_entry'),
	

	

	url(r'sales_return_entry/$', SalesReturn.as_view(), name='return_entry'),

	url(r'view_sales/$', ViewSales.as_view(), name='view_sales'),



)