from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from reports.views import *

urlpatterns = patterns('',
	url(r'^reports/$', login_required(Reports.as_view()), name='reports'),
	url(r'^sales_reports/$', login_required(SalesReports.as_view()), name='sales_reports'),	
	url(r'^purchase/$', login_required(PurchaseReports.as_view()), name='purchase_reports'),
	url(r'^vendor_accounts/$', login_required(VendorAccountsReport.as_view()), name='vendor_accounts_report'),
	url(r'^stock_reports/$', login_required(StockReports.as_view()), name='stock_reports'),
	url(r'^salesreturn_reports/$', login_required(SalesReturnReport.as_view()), name='sales_return_report'),
	url(r'^daily_report/$', login_required(DailyReport.as_view()), name='daily_report'),
	url(r'^purchase_return/$', login_required(PurchaseReturnReport.as_view()), name='purchase_return_report'),
	url(r'^expenses/$', login_required(ExpenseReport.as_view()), name='expense_report'),
)
