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

from sales.models import Sales, SalesItem, SalesReturn
from inventory.models import Item, Inventory
from web.models import Customer, Staff

class SalesEntry(View):
    def get(self, request, *args, **kwargs):
        current_date = dt.datetime.now().date()
        sales_invoice_number = Sales.objects.aggregate(Max('sales_invoice_number'))['sales_invoice_number__max']
        
        if not sales_invoice_number:
            sales_invoice_number = 1
        else:
            sales_invoice_number = sales_invoice_number + 1
        return render(request, 'sales/sales_entry.html',{
            'sales_invoice_number': sales_invoice_number,
            'current_date': current_date.strftime('%d/%m/%Y'),
        })

    def post(self, request, *args, **kwargs):

        
        sales_dict = ast.literal_eval(request.POST['sales'])
        sales, sales_created = Sales.objects.get_or_create(sales_invoice_number=sales_dict['sales_invoice_number'])
        sales.sales_invoice_number = sales_dict['sales_invoice_number']
        sales.sales_invoice_date = datetime.strptime(sales_dict['sales_invoice_date'], '%d/%m/%Y')
        customer = Customer.objects.get(user__first_name=sales_dict['customer'])
        
        salesman = Staff.objects.get(user__first_name=sales_dict['staff']) 
        
        sales.discount = sales_dict['net_discount']
        sales.round_off = sales_dict['roundoff']
        sales.net_amount = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
        sales.customer = customer
        sales.salesman = salesman
        
        sales.save()
        sales_items = sales_dict['sales_items']
        for sales_item in sales_items:
           
            item = Item.objects.get(code=sales_item['item_code'])
            s_item, item_created = SalesItem.objects.get_or_create(item=item, sales=sales)
            inventory, created = Inventory.objects.get_or_create(item=item)
            if sales_created:
                print "sadjohsjalfhls";
                inventory.quantity = inventory.quantity - int(sales_item['qty_sold'])
            else:
                inventory.quantity = inventory.quantity + s_item.quantity_sold - int(sales_item['qty_sold'])
                

            inventory.save()

                    
            s_item, item_created = SalesItem.objects.get_or_create(item=item, sales=sales)
            s_item.sales = sales
            s_item.item = item
            s_item.quantity_sold = sales_item['qty_sold']
            s_item.discount_given = sales_item['disc_given']
            s_item.net_amount = sales_item['net_amount']
            s_item.save()
                    
        res = {
            'result': 'Ok',
        }
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")
    

class SalesReturnView(View):
    def get(self, request, *args, **kwargs):
        return_invoice_number = SalesReturn.objects.aggregate(Max('return_invoice_number'))['return_invoice_number__max']
        
        if not return_invoice_number:
            return_invoice_number = 1
        else:
            return_invoice_number = return_invoice_number + 1
        return render(request, 'sales/return_entry.html',{
            'return_invoice_number': return_invoice_number
        })

    def post(self, request, *args, **kwargs):
    	# salesreturn = SalesReturn()
    	# salesreturn.sales =sales_created request.POST['sales']
    	# salesreturn.date = request.POST['date']
    	# salesreturn.total = request.POST['total']
    	# salesreturn.discount = request.POST['discount']
    	# salesreturn.round_off = request.POST['round_off']
    	# salesreturn.grand_total = request.POST['grand_total']
    	# salesreturn.save()

    	return render(request, 'sales/return_entry.html',{})

  	
class ViewSales(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sales/view_sales.html',{})

class SalesDetails(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            invoice_number = request.GET['invoice_no']
            sales = Sales.objects.get(sales_invoice_number=invoice_number)
            sales_items = SalesItem.objects.filter(sales=sales)

            sl_items = []

            for item in sales_items:
                sl_items.append({
                    'item_code': item.item.code,
                    'item_name': item.item.name,
                    'barcode': item.item.barcode,
                    'stock': item.item.inventory_set.all()[0].quantity,
                    'unit_price': item.item.inventory_set.all()[0].selling_price,
                    'uom': item.item.uom,
                    'quantity_sold': item.quantity_sold,
                    'discount_given': item.discount_given

                })
            sales_dict = {
                'invoice_number': sales.sales_invoice_number,
                'sales_invoice_date': sales.sales_invoice_date.strftime('%d/%m/%Y'),
                'customer': sales.customer.user.first_name,
                'sales_man': sales.salesman.user.first_name,
                'net_amount': sales.net_amount,
                'round_off': sales.round_off,
                'grant_total': sales.grant_total,
                'discount': sales.discount
            }
            res = {
                'result': 'Ok',
                'sales': sales_dict
            }
            response = simplejson.dumps(res)
            status_code = 200
            return HttpResponse(response, status = status_code, mimetype="application/json")

        return render(request, 'sales/view_sales.html',{})