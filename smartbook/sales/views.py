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

from sales.models import Sales, SalesItem, SalesReturn, SalesReturnItem, Quotation, QuotationItem, DeliveryNote, SalesInvoice
from inventory.models import Item, Inventory
from web.models import Customer, Staff

class SalesEntry(View):
    def get(self, request, *args, **kwargs):
        current_date = dt.datetime.now().date()

        inv_number = SalesInvoice.objects.aggregate(Max('id'))['id__max']
        
        if not inv_number:
            inv_number = 1
            prefix = 'SI'
        else:
            inv_number = inv_number + 1
            prefix = SalesInvoice.objects.latest('id').prefix
        invoice_number = prefix + str(inv_number)

        return render(request, 'sales/sales_entry.html',{
            'sales_invoice_number': invoice_number,
            'current_date': current_date.strftime('%d/%m/%Y'),
        })

    def post(self, request, *args, **kwargs):

        
        sales_dict = ast.literal_eval(request.POST['sales'])
        sales, sales_created = Sales.objects.get_or_create(sales_invoice_number=sales_dict['sales_invoice_number'])
        sales.sales_invoice_number = sales_dict['sales_invoice_number']
        sales.sales_invoice_date = datetime.strptime(sales_dict['sales_invoice_date'], '%d/%m/%Y')
        quotation = Quotation.objects.get(reference_id=sales_dict['quotation_ref_no'])
        sales.quotation = quotation
        delivery_note = DeliveryNote.objects.get(delivery_note_number=sales_dict['delivery_no'])
        sales.delivery_note = delivery_note
        sales.customer = delivery_note.customer
        sales.save()
        # customer = Customer.objects.get(user__first_name=sales_dict['customer'])
        
        salesman = Staff.objects.get(user__first_name=sales_dict['staff']) 
        
        sales.discount = sales_dict['net_discount']
        sales.round_off = sales_dict['roundoff']
        sales.net_amount = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
        sales.customer = customer
        sales.salesman = salesman
        sales.payment_mode = sales_dict['payment_mode']
        if sales_dict['payment_mode'] == 'card':
            sales.card_number = sales_dict['card_number']
            sales.bank_name = sales_dict['bank_name']
        sales.save()
        sales_items = sales_dict['sales_items']
        for sales_item in sales_items:
           
            item = Item.objects.get(code=sales_item['item_code'])
            s_item, item_created = SalesItem.objects.get_or_create(item=item, sales=sales)
            # inventory, created = Inventory.objects.get_or_create(item=item)
            # if sales_created:
            #     inventory.quantity = inventory.quantity - int(sales_item['qty_sold'])
            # else:
            #     inventory.quantity = inventory.quantity + s_item.quantity_sold - int(sales_item['qty_sold'])
                

            # inventory.save()

                    
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
        if SalesReturn.objects.exists():
            invoice_number = int(SalesReturn.objects.aggregate(Max('return_invoice_number'))['return_invoice_number__max']) + 1
        else:
            invoice_number = 1
        if not invoice_number:
            invoice_number = 1
        return render(request, 'sales/return_entry.html', {
            'invoice_number' : invoice_number,
        })

    def post(self, request, *args, **kwargs):


        post_dict = request.POST['sales_return']

        post_dict = ast.literal_eval(post_dict)
        sales = Sales.objects.get(sales_invoice_number=post_dict['sales_invoice_number'])
        sales_return, created = SalesReturn.objects.get_or_create(sales=sales, return_invoice_number = post_dict['invoice_number'])
        sales_return.date = datetime.strptime(post_dict['sales_return_date'], '%d/%m/%Y')
        sales_return.net_amount = post_dict['net_return_total']
        sales_return.save()
        
        

        return_items = post_dict['sales_items']

        for item in return_items:
            return_item = Item.objects.get(code=item['item_code'])
            s_return_item, created = SalesReturnItem.objects.get_or_create(item=return_item, sales_return=sales_return)
            s_return_item.amount = item['returned_amount']
            s_return_item.return_quantity = item['returned_quantity']
            s_return_item.save()

            inventory = Inventory.objects.get(item=return_item)
            inventory.quantity = inventory.quantity + int(item['returned_quantity'])
            inventory.save()
        response = {
                'result': 'Ok',
            }
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

  	
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
                    'tax': item.item.tax,
                    'uom': item.item.uom.uom,
                    'quantity_sold': item.quantity_sold,
                    'discount_given': item.discount_given,


                })
            sales_dict = {
                'invoice_number': sales.sales_invoice_number,
                'sales_invoice_date': sales.sales_invoice_date.strftime('%d/%m/%Y'),
                'customer': sales.customer.user.first_name,
                'sales_man': sales.salesman.user.first_name,
                'net_amount': sales.net_amount,
                'round_off': sales.round_off,
                'grant_total': sales.grant_total,
                'discount': sales.discount,
                'sales_items': sl_items
            }
            res = {
                'result': 'Ok',
                'sales': sales_dict
            }
            response = simplejson.dumps(res)
            status_code = 200
            return HttpResponse(response, status = status_code, mimetype="application/json")

        return render(request, 'sales/view_sales.html',{})

class CreateQuotation(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()

        ref_number = Quotation.objects.aggregate(Max('id'))['id__max']
        
        if not ref_number:
            ref_number = 1
            prefix = 'QO'
        else:
            ref_number = ref_number + 1
            prefix = Quotation.objects.latest('id').prefix
        reference_number = prefix + str(ref_number)

        context = {
            'current_date': current_date.strftime('%d-%m-%Y'),
            'reference_number': reference_number,
        }

        return render(request, 'sales/create_quotation.html', context)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            quotation_data = ast.literal_eval(request.POST['quotation'])
            quotation, quotation_created = Quotation.objects.get_or_create(reference_id=quotation_data['reference_no'])
            quotation.date = datetime.strptime(quotation_data['date'], '%d-%m-%Y')
            quotation.attention = quotation_data['attention']
            quotation.subject = quotation_data['subject']
            quotation.net_total = quotation_data['total_amount']
            quotation.save()
            customer = Customer.objects.get(customer_name=quotation_data['customer'])
            quotation.to = customer
            quotation.save()

            quotation_data_items = quotation_data['sales_items']
            for quotation_item in quotation_data_items:
                item = Item.objects.get(code=quotation_item['item_code'])
                quotation_item_obj, item_created = QuotationItem.objects.get_or_create(item=item, quotation=quotation)
                inventory, created = Inventory.objects.get_or_create(item=item)
                if quotation_created:
                    inventory.quantity = inventory.quantity - int(quotation_item['qty_sold'])
                else:
                    inventory.quantity = inventory.quantity + quotation_item_obj.quantity_sold - int(sales_item['qty_sold'])
                inventory.save()
                quotation_item_obj.net_amount = float(quotation_item['net_amount'])
                quotation_item_obj.quantity_sold = int(quotation_item['qty_sold'])
                quotation_item_obj.save()
            res = {
                'result': 'OK',
            }

            response = simplejson.dumps(res)

            return HttpResponse(response, status=200, mimetype='application/json')

class CreateDeliveryNote(View):

    def get(self, request, *args, **kwargs):

        current_date = dt.datetime.now().date()

        ref_number = DeliveryNote.objects.aggregate(Max('id'))['id__max']
        
        if not ref_number:
            ref_number = 1
            prefix = 'DN'
        else:
            ref_number = ref_number + 1
            prefix = DeliveryNote.objects.latest('id').prefix
        delivery_no = prefix + str(ref_number)

        context = {
            'current_date': current_date.strftime('%d-%m-%Y'),
            'delivery_no': delivery_no,
        }

        return render(request, 'sales/create_delivery_note.html', context)

    def post(self, request, *args, **kwargs):

        if request.is_ajax():

            delivery_note_details = ast.literal_eval(request.POST['delivery_note'])
            quotation = Quotation.objects.get(reference_id=delivery_note_details['quotation_no'])
            delivery_note = DeliveryNote.objects.create(quotation=quotation)
            quotation.processed = True
            quotation.save()
            delivery_note.quotation = quotation
            delivery_note.customer = quotation.to
            delivery_note.date = datetime.strptime(delivery_note_details['date'], '%d-%m-%Y')
            delivery_note.lpo_number = delivery_note_details['lpo_no']
            delivery_note.delivery_note_number = delivery_note_details['delivery_note_no']
            delivery_note.save()

            res = {
                'result': 'ok',

            }

            response = simplejson.dumps(res)

            return HttpResponse(response, status=200, mimetype='application/json')

class QuotationDetails(View):

    def get(self, request, *args, **kwargs):

        ref_number = request.GET.get('reference_no', '')

        quotations = Quotation.objects.filter(reference_id__istartswith=ref_number)
        quotation_list = []
        for quotation in quotations:
            item_list = []
            i = 0 
            i = i + 1
            for q_item in quotation.quotationitem_set.all():
                item_list.append({
                    'sl_no': i,
                    'item_name': q_item.item.name,
                    'item_code': q_item.item.code,
                    'barcode': q_item.item.barcode,
                    'item_description': q_item.item.description,
                    'qty_sold': q_item.quantity_sold,
                    'tax': q_item.item.tax,
                    'uom': q_item.item.uom.uom,
                    'current_stock': q_item.item.inventory_set.all()[0].quantity if q_item.item.inventory_set.count() > 0  else 0 ,
                    'selling_price': q_item.item.inventory_set.all()[0].selling_price if q_item.item.inventory_set.count() > 0 else 0 ,
                    'discount_permit': q_item.item.inventory_set.all()[0].discount_permit_percentage if q_item.item.inventory_set.count() > 0 else 0,
                    'net_amount': q_item.net_amount,
                })
                i = i + 1
            quotation_list.append({
                'ref_no': quotation.reference_id,
                'customer': quotation.to.customer_name if quotation.to else '' ,
                'items': item_list,
                'net_total': quotation.net_total,
                'delivery_no': quotation.deliverynote_set.all()[0].delivery_note_number if quotation.deliverynote_set.all().count() > 0 else 0,
            })
        res = {
            'quotations': quotation_list,
            'result': 'ok',
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')

class DeliveryNoteDetails(View):

    def get(self, request, *args, **kwargs):

        delivery_no = request.GET.get('delivery_no', '')

        delivery_note_details = DeliveryNote.objects.filter(delivery_note_number__istartswith=delivery_no)
        delivery_note_list = []

        for delivery_note in delivery_note_details:
            i = 0 
            i = i + 1
            item_list = []
            for q_item in delivery_note.quotation.quotationitem_set.all():
                    item_list.append({
                        'sl_no': i,
                        'item_name': q_item.item.name,
                        'item_code': q_item.item.code,
                        'barcode': q_item.item.barcode,
                        'item_description': q_item.item.description,
                        'qty_sold': q_item.quantity_sold,
                        'tax': q_item.item.tax,
                        'uom': q_item.item.uom.uom,
                        'current_stock': q_item.item.inventory_set.all()[0].quantity if q_item.item.inventory_set.count() > 0  else 0 ,
                        'selling_price': q_item.item.inventory_set.all()[0].selling_price if q_item.item.inventory_set.count() > 0 else 0 ,
                        'discount_permit': q_item.item.inventory_set.all()[0].discount_permit_percentage if q_item.item.inventory_set.count() > 0 else 0,
                        'net_amount': q_item.net_amount,
                    })
                    i = i + 1
            delivery_note_list.append({
                'ref_no': delivery_note.quotation.reference_id,
                'customer': delivery_note.quotation.to.customer_name if delivery_note.quotation.to else '' ,
                'items': item_list,
                'net_total': delivery_note.quotation.net_total,
                'delivery_no': delivery_note.delivery_note_number,
            })
        res = {
            'delivery_notes': delivery_note_list,
            'result': 'ok',
        }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')



