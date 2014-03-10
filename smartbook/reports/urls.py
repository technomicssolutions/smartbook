from django.conf.urls import patterns, include, url

from reports.views import *

urlpatterns = patterns('',
	url(r'reports/$', Reports.as_view(), name='reports'),
	url(r'sales_reports_date/$', SalesReportsDate.as_view(), name='sales_reports_date'),
	url(r'sales_reports_item/$', SalesReportsItem.as_view(), name='sales_reports_item'),
	url(r'sales_reports_salesman/$', SalesReportsSalesman.as_view(), name='sales_reports_salesman'),
	url(r'sales_reports_customer/$', SalesReportsCustomer.as_view(), name='sales_reports_customer'),
	url(r'sales_reports_area/$', SalesReportsArea.as_view(), name='sales_reports_area'),

)
