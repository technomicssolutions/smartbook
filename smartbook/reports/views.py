# Create your views here.
import sys

from django.db import IntegrityError

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

