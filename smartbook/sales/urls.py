from django.conf.urls import patterns, include, url

from sales.views import *

urlpatterns = patterns('',
#	url(r'^$', Home.as_view(), name='home'),
	url(r'sales/$', Sales.as_view(), name='sales'),
	url(r'sales_reports/$', Sales_reports.as_view(), name='sales_reports'),

)