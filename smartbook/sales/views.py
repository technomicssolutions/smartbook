# Create your views here.
import sys

from django.db import IntegrityError
from django.db.models import Max
from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from sales.models import Sales

#from sales.models import *

class SalesEntry(View):
	def get(self, request, *args, **kwargs):
		sales_invoice_number = Sales.objects.aggregate(Max('sales_invoice_number'))['sales_invoice_number__max']
		if not sales_invoice_number:
			sales_invoice_number = 1
		return render(request, 'sales/sales_entry.html',{
			'sales_invoice_number': sales_invoice_number,
    	})
    

class SalesReturn(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sales/return_entry.html',{})

    def post(self, request, *args, **kwargs):
    	salesreturn = SalesReturn()
    	salesreturn.sales = request.POST['sales']
    	salesreturn.date = request.POST['date']
    	salesreturn.total = request.POST['total']
    	salesreturn.discount = request.POST['discount']
    	salesreturn.round_off = request.POST['round_off']
    	salesreturn.grand_total = request.POST['grand_total']
    	salesreturn.save()

    	return render(request, 'sales/return_entry.html',{})

  	
class ViewSales(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sales/view_sales.html',{})

