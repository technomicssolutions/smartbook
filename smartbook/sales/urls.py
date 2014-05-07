from django.conf.urls import patterns, include, url

from sales.views import *

urlpatterns = patterns('',

	url(r'^$', SalesDetails.as_view(), name='sales_details'),	
	url(r'^entry/$', SalesEntry.as_view(), name='sales'),
	url(r'^return/$', SalesReturnView.as_view(), name='return_entry'),	
	#url(r'sales_return_entry/$', SalesReturnView.as_view(), name='return_entry'),
	url(r'view_sales/$', ViewSales.as_view(), name='view_sales'),
	url(r'create_quotation/$', CreateQuotation.as_view(), name='create_quotation'),
	url(r'^create_quotation_pdf/(?P<quotation_id>\d+)/$', CreateQuotationPdf.as_view(), name='create_quotation_pdf'),

)