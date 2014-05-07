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
from django.conf import settings

from sales.models import Sales, SalesItem, SalesReturn, SalesReturnItem, Quotation, QuotationItem, DeliveryNote, SalesInvoice
from inventory.models import Item, Inventory
from web.models import Customer, Staff, OwnerCompany

from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.http import HttpResponse

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
        if sales_dict['delivery_no'] is not 0:
            delivery_note, delivery_note_created = DeliveryNote.objects.get_or_create(delivery_note_number=sales_dict['delivery_no'], quotation=quotation)
        # if delivery_note_created:
        #     delivery_note.customer = quotation.to
        #     delivery_note.date = datetime.strptime(sales_dict['sales_invoice_date'], '%d/%m/%Y')
            
        #     ref_number = DeliveryNote.objects.aggregate(Max('id'))['id__max']
        #     if not ref_number:
        #         ref_number = 1
        #         prefix = 'DN'
        #     else:
        #         ref_number = ref_number + 1
        #         prefix = DeliveryNote.objects.latest('id').prefix
        #     delivery_no = prefix + str(ref_number)
        #     delivery_note.delivery_note_number = delivery_no
        #     delivery_note.save()

            sales.delivery_note = delivery_note
        sales.customer = quotation.to
        sales.save()

        salesman = Staff.objects.get(user__first_name=sales_dict['staff']) 
        
        sales.discount = sales_dict['net_discount']
        sales.round_off = sales_dict['roundoff']
        sales.net_amount = sales_dict['net_total']
        sales.grant_total = sales_dict['grant_total']
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


        # Creating sales invoice 

        sales_invoice = SalesInvoice.objects.create(quotation=quotation, sales=sales)
        if sales_dict['delivery_no'] is not 0:
            delivery_note.processed = True
            delivery_note.save()
        quotation.is_sales_invoice_created = True
        quotation.save()
        if sales_dict['delivery_no'] is not 0:
            sales.delivery_note = delivery_note
        sales.quotation = quotation
        sales.save()
        sales_invoice.sales = sales
        if sales_dict['delivery_no'] is not 0:
            sales_invoice.delivery_note = delivery_note
        sales_invoice.quotation = quotation
        sales_invoice.date = datetime.strptime(sales_dict['sales_invoice_date'], '%d/%m/%Y')
        sales_invoice.customer = quotation.to
        sales_invoice.invoice_no = sales_dict['sales_invoice_number']
        sales_invoice.save()

                    
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
                'quotation_id': quotation.id,
            }

            response = simplejson.dumps(res)

            return HttpResponse(response, status=200, mimetype='application/json')

class DeliveryNotePDF(View):
     def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))

        status_code = 200

        y=850

        # p.drawString(100, 950, "SUNLIGHT STATIONARY")
        # p.drawString(100, 930, "Colour Printing, Photo Copy, Spiral Binding")
        # p.drawString(100, 910, "Tender Document and Printing Service")
        # p.drawString(100, 890, "Tel. : +971-2-6763571")
        # p.drawString(100, 870, "Fax : +971-2-6763581")
        # p.drawString(100, 850, "E-mail : sunlight.stationary@yahoo.com")
        # p.drawString(100, 830, "P.O.Box : 48296")
        # p.drawString(100, 810, "Behind Russian Embassy")
        # p.drawString(100, 790, "Ziyani, Abu Dhabi, U.A.E.")
        # p.drawString(100, 700, "No.  ")
        # p.drawString(700, 700, "Date : ....................................")
        # p.drawString(700, 680, "L.P.O. No : ............................")
        # p.drawString(100, 650, "Mr.M/s.......................................................................................................................................................................................................................")

        # data=[['Sl.No:', 'Description', 'Qty', 'Remarks']]

        table = Table(data, colWidths=[100, 400, 100, 150], rowHeights=40)
        table.setStyle(TableStyle([
                                   # ('INNERGRID', (0,0), (0,0), 0.25, colors.black),
                                   # ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
                                   ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                   # ('LINEBEFORE',(1,1), (-1,-1),1,colors.black),
                                   # ('BACKGROUND',(0,0),(1,0),colors.lightgrey),
                                   ('ALIGN', (1,1), (-1,-1),'CENTRE'),
                                   ]))
        table.wrapOn(p, 200, 400)
        table.drawOn(p,105,500)

        data1=[['', '', '', '']]
        table = Table(data1, colWidths=[100, 400, 100, 150], rowHeights=40)
        table.setStyle(TableStyle([
                                   # ('INNERGRID', (0,0), (0,0), 0.25, colors.black),
                                   # ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
                                   ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                                   # ('BACKGROUND',(0,0),(1,0),colors.lightgrey)
                                   ]))
        table.wrapOn(p, 200, 400)
        table.drawOn(p,105,460)


        p.showPage()
        p.save()
        return response


class CreateQuotationPdf(View):
    def get(self, request, *args, **kwargs):

        quotation_id = kwargs['quotation_id']
        quotation = Quotation.objects.get(id=quotation_id)

        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))

        status_code = 200
        y = 850

        # p.drawInlineImage(self, 1.jpg, 80,y, width=None,height=None)
        # owner_company = OwnerCompany.objects.latest('id')
        # path = settings.PROJECT_ROOT+"/media/"+owner_company.logo.name
        # p.drawImage(path, 7*cm, 30*cm, width=20*cm, preserveAspectRatio=True)


        # p.roundRect(80, y-130, 840, 0.5*inch, 10, stroke=1, fill=0)
        # p.drawString(400, 735, "QUOTATION")
        # p.roundRect(80, y-250, 840, 120, 20, stroke=1, fill=0)   


        data=[['                      ', quotation.to.customer_name]]
        table = Table(data, colWidths=[100, 400], rowHeights=40)      
        table.wrapOn(p, 200, 400)
        table.drawOn(p,160, 680)

        data=[['                      ', quotation.attention]]
        table = Table(data, colWidths=[100, 400], rowHeights=40)       
        table.wrapOn(p, 200, 400)
        table.drawOn(p,160, 650)

        data=[['                      ', quotation.subject]]
        table = Table(data, colWidths=[100, 400], rowHeights=40)       
        table.wrapOn(p, 200, 400)
        table.drawOn(p,160, 620)


        data=[['                  ', quotation.date.strftime('%d-%m-%Y')]]
        table = Table(data, colWidths=[100, 400], rowHeights=40)       
        table.wrapOn(p, 200, 400)
        table.drawOn(p,700, 680)

        data=[['                   ', quotation.reference_id]]
        table = Table(data, colWidths=[100, 400], rowHeights=40)        
        table.wrapOn(p, 200, 400)
        table.drawOn(p,700, 650)


        # data=[['Sl.No:', 'Description', 'Qty', 'Unit Price', 'Amount(AED)']]

        # table = Table(data, colWidths=[100, 400, 100, 100, 100], rowHeights=40)
        # # table.setStyle(TableStyle([                                  
        # #                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        # #                            ('LINEBEFORE',(1,0), (0,-1),1,colors.black),                                  
        # #                            ]))
        # table.wrapOn(p, 200, 400)
        # table.drawOn(p,105,500)

        x=500

        i = 0 
        i = i + 1

        for q_item in quotation.quotationitem_set.all():
            

            x=x-40

            data1=[[i, q_item.item.description, q_item.quantity_sold, q_item.item.inventory_set.all()[0].unit_price, q_item.net_amount]]
            table = Table(data1, colWidths=[100, 400, 100, 100, 100], rowHeights=40)
            # table.setStyle(TableStyle([
            #                            # ('INNERGRID', (0,0), (0,0), 0.25, colors.black),
            #                            # ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
            #                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            #                            # ('BACKGROUND',(0,0),(1,0),colors.lightgrey)
            #                            ]))
            # table.wrapOn(p, 300, 200)
            table.wrapOn(p, 200, 400)
            # table.drawOn(p,105,460)
            table.drawOn(p,105, x)
            i = i + 1

        data=[['', quotation.net_total]]

        table = Table(data, colWidths=[700, 100], rowHeights=40)
        # table.setStyle(TableStyle([
        #                            # ('INNERGRID', (0,0), (0,0), 0.25, colors.black),
        #                            # ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
        #                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
        #                            # ('BACKGROUND',(0,0),(1,0),colors.lightgrey),
        #                            ('ALIGN', (0,0), (-1,-1),'RIGHT'),
        #                            ]))
        table.wrapOn(p, 200, 400)
        table.drawOn(p,105,x-40)

        # p.drawString(160, x-80, "Hope the above quoted prices will meet your satisfaction and for further information please do not hesitate to contact us.")
        # p.drawString(160, 220, "For")
        # p.drawString(160, 200, "Sunlight Stationary")
        # p.drawString(160, 120, "Authorized Signatory")
        # p.drawString(700, 120, "Prepared By")

        # data=[['Tel: +971-2-6763571, Fax : +971-2-6763581,P.O.Box : 48296, Abu Dhabi, United Arab Emirates']]
        # table = Table(data, colWidths=[700], rowHeights=30)
        # table.setStyle(TableStyle([
        #                            # ('BOX', (0,0), (-1,-1), 0.25, colors.black),   
        #                            ('ALIGN',(0,0), (-1,-1),'CENTRE'),                                    
        #                            ]))
       
        # table.wrapOn(p, 200, 400)
        # table.drawOn(p,160, 50)

        p.showPage()
        p.save()
        return response

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
            delivery_note, created = DeliveryNote.objects.get_or_create(quotation=quotation)
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
        in_sales_invoice_creation = ''
        sales_invoice_creation = request.GET.get('sales_invoice', '')
        
        if sales_invoice_creation == 'true':
            quotations = Quotation.objects.filter(reference_id__istartswith=ref_number, is_sales_invoice_created=False)
        else:
            quotations = Quotation.objects.filter(reference_id__istartswith=ref_number, processed=False)
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

        delivery_note_details = DeliveryNote.objects.filter(delivery_note_number__istartswith=delivery_no, processed=False)
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
