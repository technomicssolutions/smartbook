# Create your views here.
import sys

from django.db import IntegrityError
import simplejson
from datetime import datetime
from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Reports(View):
	def get(self, request, *args, **kwarg):
		return render(request, 'reports/report.html', {})

class SalesReports(View):
    def get(self, request, *args, **kwarg):
        return render(request, 'reports/sales_reports_date.html', {})

class SalesReportsDate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/sales_reports_date.html',{})        

class SalesReportsItem(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/sales_reports_item.html',{})    

class SalesReportsSalesman(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/sales_reports_salesman.html',{})

class SalesReportsCustomer(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/sales_reports_customer.html',{})	

class SalesReportsArea(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/sales_reports_area.html',{})

class PurchaseReportsDate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_reports_date.html',{})

class PurchaseReportsVendor(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_reports_vendor.html',{})	

class PurchaseAccountsDate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_accounts_date.html',{})	

class StockReportsDate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/stock_reports_date.html',{})

class SalesReturn(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/sales_return.html',{})

class DailyReport(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            status_code = 200

            print " In DailyReport View"
            start = request.GET['start_date']
            end = request.GET['end_date']
            print "start", start
            print "end", end
            start_date = datetime.strptime(start, '%d/%m/%Y')
            end_date = datetime.strptime(end, '%d/%m/%Y')
            print start_date
            print end_date
            
            try:
                
                res = {
                    'result': 'ok',                    
                }    
                response = simplejson.dumps(res)
            except Exception as ex:
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                status_code = 500
            return HttpResponse(response, status = status_code, mimetype = 'application/json')
        else:
            return render(request, 'reports/daily_report.html',{})

class PurchaseReturn(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_return.html',{})

class ExpenseReport(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/expense_report.html',{})

class PurchaseAccountsDate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_accounts_date.html',{})

class PurchaseAccountsVendor(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_accounts_vendor.html',{})

class Stock(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/stock.html',{})


# class ViewDailyReport(View):
#     def get(self, request, *args, **kw):
#         print " In DailyReport View"
#         start = request.GET['start_date']
#         end = request.GET['end_date']

#         print "start", start
#         print "end", end
#         print "HI.............."


#         return HttpResponse(simplejson.dumps({
#             'success' : 'success',             
#         }),status=200, mimetype='application/json')






