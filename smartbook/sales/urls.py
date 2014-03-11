from django.conf.urls import patterns, include, url

from sales.views import *

urlpatterns = patterns('',
#	url(r'^$', Home.as_view(), name='home'),

	url(r'sales/$', Sales.as_view(), name='sales'),
	url(r'sales_entry/$', Sales.as_view(), name='sales_entry'),
	url(r'return_entry/$', ReturnEntry.as_view(), name='return_entry'),
	url(r'view_sales/$', ViewSales.as_view(), name='view_sales'),



)