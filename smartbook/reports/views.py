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
from web.models import Vendor


from purchase.models import Purchase

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


def createPDF(purchases):

    x=85
    y=700
    buffer=StringIO()
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
    return pdf

class Reports(View):
	def get(self, request, *args, **kwarg):
		return render(request, 'reports/report.html', {})

class SalesReports(View):
    def get(self, request, *args, **kwarg):
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






