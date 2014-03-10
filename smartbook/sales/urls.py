from django.conf.urls import patterns, include, url

from sales.views import *

urlpatterns = patterns('',
#	url(r'^$', Home.as_view(), name='home'),
	url(r'sales_entry/$', Sales.as_view(), name='sales_entry'),
	url(r'sales_return/$', SalesReturn.as_view(), name='sales_return'),
	url(r'view_sales/$', ViewSales.as_view(), name='view_sales'),
	url(r'sales_reports/$', Sales_reports.as_view(), name='sales_reports'),

)