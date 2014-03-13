# Create your views here.
import sys
import ast
import simplejson
import datetime as dt
from datetime import datetime

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
from sales.models import Customer
from sales.models import Staff
#from sales.models import *

class SalesEntry(View):
    def get(self, request, *args, **kwargs):
        sales_invoice_number = Sales.objects.aggregate(Max('sales_invoice_number'))['sales_invoice_number__max']
        if not sales_invoice_number:
            sales_invoice_number = 1
        return render(request, 'sales/sales_entry.html',{
            'sales_invoice_number': sales_invoice_number,
        })

    def post(self, request, *args, **kwargs):

        print "wkjahlfkjwhkljewk"
        sales_dict = ast.literal_eval(request.POST['sales'])
        sales,sales_created = Sales.objects.get_or_create(sales_invoice_number=1)
        sales.sales_invoice_number = sales_dict['sales_invoice_number']
        sales.sales_invoice_date = datetime.strptime(sales_dict['sales_invoice_date'], '%d/%m/%Y')
        customer = Customer.objects.get(user__first_name=sales_dict['customer'])
        salesman = Staff.objects.get(user__first_name=sales_dict['staff'])      
        sales.discount = sales_dict['net_discount']
        sales.round_off = sales_dict['roundoff']
        sales.net_total = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
        
        sales.save()
        sales_items = sales_dict['sales_items']
        for sales_item in sales_items:

            item = Item.objects.get(code=sales_item['item_code'])
            s_item, item_created = salesItem.objects.get_or_create(item=item, sales=sales)
            inventory, created = Inventory.objects.get_or_create(item=item)
            if sales_created:
                inventory.quantity = inventory.quantity - int(sales_item['qty_sold'])
            else:
                inventory.quantity = inventory.quantity + int(sales_item['qty_sold'])
                inventory.quantity = inventory.quantity - int(sales_item['qty_sold'])

            inventory.save()

                    
            s_item, item_created = salesItem.objects.get_or_create(item=item, sales=sales)
            s_item.sales = sales
            s_item.item = item
            s_item.quantity_sold = sales_item['qty_sold']
            s_item.item_disc_given = sales_item['disc_given']
            s_item.net_amount = sales_item['net_amount']
            s_item.save()
                    
        res = {
            'result': 'Ok',
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")
    

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

