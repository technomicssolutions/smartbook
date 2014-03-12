from django.conf.urls import patterns, include, url

from reports.views import *

urlpatterns = patterns('',
	url(r'^reports/$', Reports.as_view(), name='reports'),
	url(r'^sales_reports_date/$', SalesReports.as_view(), name='sales_reports_date'),
	url(r'^sales_reports_date/$', SalesReportsDate.as_view(), name='sales_reports_date'),
	url(r'^sales_reports_item/$', SalesReportsItem.as_view(), name='sales_reports_item'),
	url(r'^sales_reports_salesman/$', SalesReportsSalesman.as_view(), name='sales_reports_salesman'),
	url(r'^sales_reports_customer/$', SalesReportsCustomer.as_view(), name='sales_reports_customer'),
	url(r'^sales_reports_area/$', SalesReportsArea.as_view(), name='sales_reports_area'),
	url(r'^purchase/$', PurchaseReportsDate.as_view(), name='purchase_reports'),
	url(r'^purchase_accounts_date/$', PurchaseAccountsDate.as_view(), name='purchase_accounts_date'),
	url(r'^purchase_accounts_vendor/$', PurchaseAccountsVendor.as_view(), name='purchase_accounts_vendor'),
	url(r'^stock_reports_date/$', StockReportsDate.as_view(), name='stock_reports_date'),
	url(r'^sales_return/$', SalesReturn.as_view(), name='sales_return'),
	url(r'^daily_report/$', DailyReport.as_view(), name='daily_report'),
	url(r'^purchase_return/$', PurchaseReturn.as_view(), name='purchase_return'),
	url(r'^expense_report/$', ExpenseReport.as_view(), name='expense_report'),
	url(r'^stock/$', Stock.as_view(), name='stock'),	

)
