# Create your views here.
import sys
import os
import os.path

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
from django.conf import settings

from sales.models import Sales, SalesItem
from expenses.models import Expense
from inventory.models import *
from purchase.models import PurchaseItem
from django.core.files import File

from purchase.models import Purchase, VendorAccount
from reports.models import ReportTest

from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Image, Table, TableStyle
from reportlab.lib import colors

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate


from reportlab.pdfgen import canvas
from django.http import HttpResponse


def generate(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # # Create the PDF object, using the response object as its "file."
    # p = canvas.Canvas(response)

    # # Draw things on the PDF. Here's where the PDF generation happens.
    # # See the ReportLab documentation for the full list of functionality.
    # p.drawString(100, 100, "Hello world.")

    # # Close the PDF object cleanly, and we're done.
    # p.showPage()
    # p.save()
    # return response
    x=85
    y=700
    buffer=StringIO()
    doc = SimpleDocTemplate(buffer) 
    p=canvas.Canvas(buffer,pagesize=letter)
    #p = canvas.Canvas("myreport.pdf")
    # path = settings.PROJECT_PATH + '/../web/static/img/logo.png'
    # p.drawImage(path, 3*cm, 25*cm, width=5*cm, preserveAspectRatio=True)
    p.drawString(x, y, "Sportivore Pty. Ltd.")
    y = 680
    p.drawString(x, y, "ACN  166 877 818")
    y = 660
    p.drawString(x, y, "Phone   +61 424 367 235")
    y = 640
    p.drawString(x, y, "Email   admin@sportivore.com.au")
    data=[['Receipt'],['Date invoiced', str(datetime.now().date())], ['Payment Id', 'tset'], ['User name', 'test'+' '+'test']]
    table = Table(data, colWidths=[100, 215], rowHeights=30)
    table.setStyle(TableStyle([
                               ('INNERGRID', (0,0), (0,0), 0.25, colors.black),
                               ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('BACKGROUND',(0,0),(1,0),colors.lightgrey)
                               ]))
    table.wrapOn(p, 200, 400)
    table.drawOn(p,85,500)
    # game_detail = game.date.strftime('%A, %dth of %B')+ " - " +"game.start_time.strftime('%I %p')"+' - '+ game.sport.title+ ' at '+ game.court.venue.venue_name
    data=[['Game Details', 'Amount'],['game_detail, game.cost'], ['Amount Paid', 'game.cost']]
    table = Table(data, colWidths=[300, 100], rowHeights=[30, 70, 30])
    table.setStyle(TableStyle([
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('BACKGROUND',(0,0),(1,0),colors.lightgrey),
                               ('VALIGN',(0, 1),(-1,-1),'TOP'),
                               ('ALIGN',(0, 2),(-1,-1),'RIGHT')
                               ]))
    table.wrapOn(p, 200, 450)
    table.drawOn(p,85,350)
    p.showPage()
    p.save() 
    pdf=buffer.getvalue()
    buffer.close()
    doc.build(document)  
    myfile = ContentFile(pdf) 

    m = ReportTest()
    m.file_name.save('test.pdf', myfile) 

    response.write(pdf)
    print response.FILES
    return response


def createPDF(purchases):

    
    return pdf

class Reports(View):
	def get(self, request, *args, **kwarg):
		return render(request, 'reports/report.html', {})

class SalesReports(View):
    def get(self, request, *args, **kwarg):

        if request.is_ajax():
            status_code = 200
            sales_report = []
            total_sales_report = []
            round_off = 0
            grant_total = 0
            total_profit = 0
            total_discount = 0
            total_cp = 0
            total_sp = 0
            cost_price = 0
            i = 0 
            

            if request.GET['report_name'] == 'date':
                start = request.GET['start_date']
                end = request.GET['end_date']            
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date)
                if sales.count()>0:
                    for sale in sales:
                        round_off = round_off + sale.round_off
                        items = sale.salesitem_set.all()
                        for item in items:
                            discount = item.discount_given                         
                            dates = item.sales.sales_invoice_date
                            invoice_no = item.sales.sales_invoice_number
                            qty = item.quantity_sold
                            item_name = item.item.name
                            inventorys = item.item.inventory_set.all()[0]                            
                            selling_price = inventorys.selling_price

                            purchases = item.item.purchaseitem_set.all()
                            if purchases.count()>0:                                
                                for purchase in purchases:                                
                                    cost_price = cost_price + purchase.cost_price
                                    i = i + 1
                                avg_cp = cost_price/i
                            total = selling_price * qty
                            profit = (selling_price - avg_cp)*qty

                            grant_total = grant_total + total
                            total_profit = total_profit + profit
                            total_discount = total_discount + discount

                            sales_report.append({
                                'dates' : dates.strftime('%d-%m-%Y'),
                                'invoice_no' : invoice_no,
                                'item_name' : item_name,
                                'qty' : qty,
                                'discount' : discount,
                                'selling_price' : selling_price,
                                'total' : total,
                                'profit' : profit,
                            })
                    total_sales_report.append({
                        'round_off' : round_off,
                        'grant_total' : grant_total,
                        'total_profit' : total_profit,
                        'total_discount' : total_discount,
                    })

            elif request.GET['report_name'] == 'item':
                start = request.GET['start_date']
                end = request.GET['end_date']            
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date)
                if sales.count()>0:
                    for sale in sales:
                        items = sale.salesitem_set.all()
                        for item in items:
                            discount = item.discount_given                         
                            total_qty = item.quantity_sold
                            item_name = item.item.name
                            item_code = item.item.code
                            inventorys = item.item.inventory_set.all()[0]
                            selling_price = inventorys.selling_price

                            purchases = item.item.purchaseitem_set.all()
                            if purchases.count()>0:
                                for purchase in purchases:
                                    cost_price = cost_price + purchase.cost_price
                                    i = i + 1
                                avg_cp = cost_price/i
                            profit = (selling_price - avg_cp)*total_qty

                            total_profit = total_profit + profit
                            total_discount = total_discount + discount
                            total_cp = total_cp + avg_cp
                            total_sp = total_sp + selling_price

                            sales_report.append({
                                'item_code' : item_code,
                                'item_name' : item_name,
                                'total_qty' : total_qty,
                                'discount' : discount,
                                'cost_price' : avg_cp,
                                'selling_price' : selling_price,
                                'profit' : profit,
                            })
                total_sales_report.append({
                    'total_cp' : total_cp,
                    'total_sp' : total_sp,
                    'total_profit' : total_profit,
                    'total_discount' : total_discount,
                })
            elif request.GET['report_name'] == 'customer':
                start = request.GET['start_date']
                end = request.GET['end_date']            
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')

                customer_name = request.GET['customer_name']
                customer = Customer.objects.get(user__first_name = customer_name)
                sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date,customer=customer)
                if sales.count()>0:
                    for sale in sales:
                        items = sale.salesitem_set.all()
                        for item in items:
                            dates = item.sales.sales_invoice_date
                            invoice_no = item.sales.sales_invoice_number
                            item_name = item.item.name
                            qty = item.quantity_sold
                            discount = item.discount_given
                            inventorys = item.item.inventory_set.all()[0]
                            selling_price = inventorys.selling_price
                            total = selling_price * qty

                            purchases = item.item.purchaseitem_set.all()
                            if purchases.count()>0:                                
                                for purchase in purchases:
                                    cost_price = cost_price + purchase.cost_price
                                    i = i + 1
                                avg_cp = cost_price/i
                            profit = (selling_price - avg_cp)*qty

                            total_profit = total_profit + profit
                            total_discount = total_discount + discount                            
                            total_sp = total_sp + selling_price
                            grant_total = grant_total + total

                            sales_report.append({
                                'dates' : dates.strftime('%d-%m-%Y'),
                                'invoice_no' : invoice_no,
                                'item_name' : item_name,
                                'qty' : qty,
                                'discount' : discount,
                                'selling_price' : selling_price,
                                'total' : total,
                                'profit' : profit,
                            })
                total_sales_report.append({
                    'grant_total' : grant_total,
                    'total_sp' : total_sp,
                    'total_profit' : total_profit,
                    'total_discount' : total_discount,
                })

            elif request.GET['report_name'] == 'salesman':
                start = request.GET['start_date']
                end = request.GET['end_date']            
                start_date = datetime.strptime(start, '%d/%m/%Y')
                end_date = datetime.strptime(end, '%d/%m/%Y')
                
                salesman_name = request.GET['salesman_name']
                desig = Designation.objects.get(title = 'Salesman')                
                salesmen = Staff.objects.filter(designation = desig, user__first_name=salesman_name)                
                sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date,salesman=salesmen)
                
                if sales.count()>0:                    
                    for sale in sales:
                        items = sale.salesitem_set.all()
                        for item in items:
                            dates = item.sales.sales_invoice_date
                            invoice_no = item.sales.sales_invoice_number
                            item_name = item.item.name
                            qty = item.quantity_sold
                            discount = item.discount_given
                            inventorys = item.item.inventory_set.all()[0]
                            selling_price = inventorys.selling_price
                            total = selling_price * qty

                            purchases = item.item.purchaseitem_set.all()
                            if purchases.count()>0:                                
                                for purchase in purchases:
                                    cost_price = cost_price + purchase.cost_price
                                    i = i + 1
                                avg_cp = cost_price/i
                            profit = (selling_price - avg_cp)*qty

                            total_profit = total_profit + profit
                            total_discount = total_discount + discount                            
                            total_sp = total_sp + selling_price
                            grant_total = grant_total + total

                            sales_report.append({
                                'dates' : dates.strftime('%d-%m-%Y'),
                                'invoice_no' : invoice_no,
                                'item_name' : item_name,
                                'qty' : qty,
                                'discount' : discount,
                                'selling_price' : selling_price,
                                'total' : total,
                                'profit' : profit,
                            })
                total_sales_report.append({
                    'grant_total' : grant_total,
                    'total_sp' : total_sp,
                    'total_profit' : total_profit,
                    'total_discount' : total_discount,
                })            

            try:                
                res = {
                    'result': 'ok',
                    'sales_report' : sales_report,
                    'total_sales_report' : total_sales_report,
                }    
                response = simplejson.dumps(res)
            except Exception as ex:
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                status_code = 500
            return HttpResponse(response, status = status_code, mimetype = 'application/json')
        
        else:
            return render(request, 'reports/sales_reports.html', {})

class PurchaseReportsDate(View):
    def get(self, request, *args, **kwargs):

        if request.is_ajax():
            ctx_purchase_report = []
            status_code = 200
            if request.GET['report_name'] == 'date':
                
                
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                purchases = Purchase.objects.filter(purchase_invoice_date__gte=start_date, purchase_invoice_date__lte=end_date).order_by('purchase_invoice_date')

                # response = HttpResponse(content_type='application/pdf')
                # response = HttpResponse(content_type='application/pdf')

                # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

                # # Create the PDF object, using the response object as its "file."
                # temp = StringIO()
                # p = canvas.Canvas(temp)

                # # Draw things on the PDF. Here's where the PDF generation happens.
                # # See the ReportLab documentation for the full list of functionality.
                # p.drawString(100, 100, "Hello world.")

                # # Close the PDF object cleanly, and we're done.
                # p.showPage()
                # p.save()
                # response.write(temp.getvalue())
                # fileobj = File(p)
                # print type(fileobj)

                # file_extension = 'pdf'
                # path = settings.PROJECT_ROOT
                # print path
                # print 'root === ',settings.PROJECT_ROOT
                # pdf_file_name = 'purchase_report_date_wise'+"."+file_extension
                # pdf_name = path+'/media/uploads/reports/%s'%(pdf_file_name)
                # file_name = '%s'%(pdf_name)
                # print file_name
                # with open(file_name, 'w') as destination:
                #     for chunk in fileobj.chunks():
                #         destination.write(chunk)
                # file_path = "uploads/reports/"+pdf_file_name

                if len(purchases) > 0:
                    for purchase in purchases:
                        ctx_purchase_report.append({
                            'date': purchase.purchase_invoice_date.strftime('%d/%m/%Y'),
                            'invoice_no': purchase.purchase_invoice_number,
                            'vendor_invoice_no': purchase.vendor_invoice_number,
                            'item_code': purchase.purchaseitem_set.all()[0].item.code,
                            'item_name': purchase.purchaseitem_set.all()[0].item.name,
                            'uom': purchase.purchaseitem_set.all()[0].item.uom.uom,
                            'unit_cost_price': purchase.purchaseitem_set.all()[0].cost_price,
                            'quantity': purchase.purchaseitem_set.all()[0].quantity_purchased,
                            'amount': float(purchase.purchaseitem_set.all()[0].net_amount),
                        })

                        
            else:
                vendor_name = request.GET['vendor_name']
                vendor = Vendor.objects.get(user__first_name = vendor_name)
                purchases = Purchase.objects.filter(vendor = vendor)
                if len(purchases) > 0:
                    for purchase in purchases:
                        ctx_purchase_report.append({
                            'date': purchase.purchase_invoice_date.strftime('%d/%m/%Y'),
                            'invoice_no': purchase.purchase_invoice_number,
                            'vendor_invoice_no': purchase.vendor_invoice_number,
                            'amount': float(purchase.purchaseitem_set.all()[0].net_amount),
                        })
            try:    
                res = {
                    'purchases': ctx_purchase_report,                 
                }    
                response = simplejson.dumps(res)
            except Exception as ex:
                # remember to change exception
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                status_code = 500
            return HttpResponse(response, status = status_code, mimetype = 'application/json')
        else:
            return render(request, 'reports/purchase_reports.html',{})

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
            start = request.GET['start_date']
            end = request.GET['end_date']            
            start_date = datetime.strptime(start, '%d/%m/%Y')
            end_date = datetime.strptime(end, '%d/%m/%Y')
            daily_report = []
            round_off = 0
            discount = 0
            total_income = 0
            total_expense = 0
            daily_report_sales = []
            sales = Sales.objects.filter(sales_invoice_date__gte=start_date,sales_invoice_date__lte=end_date)
            if sales.count()>0:
                for sale in sales:
                    daily_report.append({
                        'income' : sale.grant_total,
                        'invoice_no' : sale.sales_invoice_number,
                        'date' : (sale.sales_invoice_date).strftime('%d-%m-%Y'),
                        'type' :True,
                    })
                    round_off = round_off+sale.round_off
                    discount = discount+sale.discount
                    total_income = total_income + sale.grant_total            
            
            expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date)
            if expenses.count()>0:
                for expense in expenses:     
                    daily_report.append({
                        'voucher_no' : expense.voucher_no,
                        'date' : (expense.date).strftime('%d-%m-%Y'),
                        'expense' : expense.amount,
                        'narration' : expense.narration,
                        'type' : False,
                        }) 
                    total_expense = total_expense + expense.amount 
            total_expense = total_expense + round_off + discount
            difference = total_income - total_expense
            daily_report_sales.append({
                'round_off' : round_off,
                'discount' : discount,
                'total_income' : total_income,
                'total_expense' : total_expense,
                'difference' : difference,
                })         
            
            try:                
                res = {
                    'result': 'ok',    
                    'daily_report' : daily_report, 
                    'daily_report_sales' : daily_report_sales,               
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
        if request.is_ajax():
            ctx_purchase_return_report = []
            status_code = 200
            if request.GET['report_name'] == 'date':
                                
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                # purchase_returns = PurchaseReturn.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
                # if len(purchase_returns) > 0:
                #     for purchase_return in purchase_returns:
                #         ctx_purchase_return_report.append({
                #             'date': purchase_return.date.strftime('%d/%m/%Y'),
                #             'vendor_name': purchase_return.vendor.user.first_name,
                #             'payment_mode': purchase_return.payment_mode,
                #             'narration': purchase_return.narration,
                #             'total_amount': purchase_return.total_amount,
                #             'paid_amount': purchase_return.paid_amount,
                #             'balance': purchase_return.balance,
                #         })
            else:
                vendor_name = request.GET['vendor_name']
                vendor = Vendor.objects.get(user__first_name = vendor_name)
                # purchase_returns = PurchaseReturn.objects.filter(vendor = vendor)
                # if len(purchase_returns) > 0:
                #     for purchasse_return in purchase_returns:
                #         ctx_purchase_return_report.append({
                #             'date': purchasse_return.date.strftime('%d/%m/%Y'),
                #             'payment_mode': purchasse_return.payment_mode,
                #             'narration': purchasse_return.narration,
                #             'total_amount': purchasse_return.total_amount,
                #             'paid_amount': purchasse_return.paid_amount,
                #             'balance': purchasse_return.balance,
                #         })
            try:    
                res = {
                    'purchase_returns': ctx_purchase_return_report,                 
                }    
                response = simplejson.dumps(res)
            except Exception as ex:
                # remember to change exception
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                status_code = 500
            return HttpResponse(response, status = status_code, mimetype = 'application/json')
        else:
            return render(request, 'reports/purchase_return.html',{})

class ExpenseReport(View):

    def get(self, request, *args, **kwargs):
        
        if request.is_ajax():
            ctx_expense_report = []
            status_code = 200
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            expenses = Expense.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
            if len(expenses) > 0: 
                for expense in expenses:
                    ctx_expense_report.append({
                        'date': expense.date.strftime('%d/%m/%Y'),
                        'particulars': expense.expense_head.expense_head,
                        'narration': expense.narration,
                        'amount': expense.amount,
                    })
            res = {
                'expenses': ctx_expense_report,
            }
            response = simplejson.dumps(res)
            return HttpResponse(response, status=status_code, mimetype='application/json')
        else:
            return render(request, 'reports/expense_report.html',{})

class PurchaseAccountsReport(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            ctx_purchase_accounts_report = []
            status_code = 200
            if request.GET['report_name'] == 'date':
                                
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                purchase_accounts = VendorAccount.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date')
                if len(purchase_accounts) > 0:
                    for purchase_account in purchase_accounts:
                        ctx_purchase_accounts_report.append({
                            'date': purchase_account.date.strftime('%d/%m/%Y'),
                            'vendor_name': purchase_account.vendor.user.first_name,
                            'payment_mode': purchase_account.payment_mode,
                            'narration': purchase_account.narration,
                            'total_amount': purchase_account.total_amount,
                            'paid_amount': purchase_account.paid_amount,
                            'balance': purchase_account.balance,
                        })
                # fileobj = createPDF(purchases)
                # file_extension = 'pdf'
                # path = settings.PROJECT_ROOT
                # print path
                # print 'root === ',settings.PROJECT_ROOT
                # pdf_file_name = 'purchase_report_date_wise'+"."+file_extension
                # pdf_name = path+'/media/uploads/reports/%s'%(pdf_file_name)
                # file_name = '%s'%(pdf_name)
                # print file_name
                # with open(file_name, 'w') as destination:
                #     for chunk in fileobj.chunks():
                #         destination.write(chunk)
                # file_path = "uploads/reports/"+pdf_file_name
            else:
                vendor_name = request.GET['vendor_name']
                vendor = Vendor.objects.get(user__first_name = vendor_name)
                purchase_accounts = VendorAccount.objects.filter(vendor = vendor)
                if len(purchase_accounts) > 0:
                    for purchase_account in purchase_accounts:
                        ctx_purchase_accounts_report.append({
                            'date': purchase_account.date.strftime('%d/%m/%Y'),
                            'payment_mode': purchase_account.payment_mode,
                            'narration': purchase_account.narration,
                            'total_amount': purchase_account.total_amount,
                            'paid_amount': purchase_account.paid_amount,
                            'balance': purchase_account.balance,
                        })
            try:    
                res = {
                    'purchase_accounts': ctx_purchase_accounts_report,                 
                }    
                response = simplejson.dumps(res)
            except Exception as ex:
                # remember to change exception
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                status_code = 500
            return HttpResponse(response, status = status_code, mimetype = 'application/json')

        else:
            return render(request, 'reports/purchase_accounts_report.html',{})

class PurchaseAccountsVendor(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_accounts_vendor.html',{})

class StockReports(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            status_code = 200
            stocks = Inventory.objects.all()
            print stocks
            ctx_stock = []
            if len(stocks) > 0:
                for stock in stocks:
                    print stock.item.purchaseitem_set.all()
                    ctx_stock.append({
                       'item_code': stock.item.code,
                       'item_name': stock.item.name,
                       'bar_code': stock.item.barcode,
                       'description': stock.item.description,
                       'brand_name': stock.item.brand.brand,
                       # 'vendor_name': stock.item.purchaseitem_set.all()[0].purchase.vendor.user.first_name,
                       'stock': stock.quantity,
                       'uom': stock.item.uom.uom,
                       'cost_price': stock.item.purchaseitem_set.all()[0].cost_price,
                       'selling_price': stock.selling_price,
                       'tax': stock.item.tax,
                       'discount': stock.discount_permit_percentage,
                       'stock_by_value': float(stock.quantity * stock.selling_price),
                       'profit': stock.selling_price - stock.item.purchaseitem_set.all()[0].cost_price,
                    })

            try:
                res = {
                    'stocks': ctx_stock,
                }
                response = simplejson.dumps(res)
            except Exception as ex:
                # remember to change exception
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                status_code = 500
            return HttpResponse(response, status = status_code, mimetype = 'application/json')

        else:
            return render(request, 'reports/stock.html',{})








