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

from sales.models import *
from expenses.models import Expense
from inventory.models import *
from purchase.models import PurchaseItem
from django.core.files import File

from purchase.models import Purchase, VendorAccount

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
                desig = Designation.objects.get(title = 'salesman')                
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
        
        ctx_purchase_report = []
        status_code = 200
        response = HttpResponse(content_type='application/pdf')
        p = canvas.Canvas(response, pagesize=(1000, 1000))
        p.setFontSize(15)
        report_type = request.GET.get('report_type', '')

        if not report_type:
            return render(request, 'reports/purchase_reports.html',{})

        if report_type == 'date':               
            p.drawCentredString(300, 900, 'Purchase Report Date wise')
            start_date = request.GET['start_date']
            end_date = request.GET['end_date']
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
            purchases = Purchase.objects.filter(purchase_invoice_date__gte=start_date, purchase_invoice_date__lte=end_date).order_by('purchase_invoice_date')
            p.setFontSize(13)
            p.drawString(50, 875, "Date")
            p.drawString(150, 875, "Invoice No")
            p.drawString(250, 875, "Vendor Invoice")
            p.drawString(350, 875, "Item code")
            p.drawString(450, 875, "Item name")
            p.drawString(550, 875, "Unit Cost price")
            p.drawString(650, 875, "Quantity")
            p.drawString(750, 875, "Amount")

            y = 850
            p.setFontSize(12)
            for purchase in purchases:
                purchase_items = purchase.purchaseitem_set.all()
                for purchase_item in purchase_items:                    
                    y = y - 30
                    p.drawString(50, y, purchase_item.purchase.purchase_invoice_date.strftime('%d/%m/%y'))
                    p.drawString(150, y, str(purchase_item.purchase.purchase_invoice_number))
                    p.drawString(250, y, str(purchase_item.purchase.vendor_invoice_number))
                    p.drawString(350, y, purchase_item.item.code)
                    p.drawString(450, y, purchase_item.item.name)
                    p.drawString(550, y, str(purchase_item.cost_price))
                    p.drawString(650, y, str(purchase_item.quantity_purchased))
                    p.drawString(750, y, str(purchase_item.net_amount))

            p.showPage()
            p.save()
        elif report_type == 'vendor':
            vendor_name = request.GET['vendor']
            vendor = Vendor.objects.get(user__first_name = vendor_name)
            purchases = Purchase.objects.filter(vendor = vendor)
            
            p.drawCentredString(300, 900, 'Purchase Report Vendor wise')
            p.setFontSize(13)
            p.drawString(50, 875, "Date")
            p.drawString(150, 875, "Invoice No")
            p.drawString(250, 875, "Vendor Invoice")
            p.drawString(750, 875, "Amount")
            p.setFontSize(12)  
            y = 850
            for purchase in purchases:
                            
                y = y - 30
                p.drawString(50, y, purchase.purchase_invoice_date.strftime('%d/%m/%y'))
                p.drawString(150, y, str(purchase.purchase_invoice_number))
                p.drawString(250, y, str(purchase.vendor_invoice_number))
                p.drawString(350, y, str(purchase.vendor_amount))
            p.showPage()
            p.save()
                  
        return response
        
class PurchaseReportsVendor(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_reports_vendor.html',{})	

class PurchaseAccountsDate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/purchase_accounts_date.html',{})	

class StockReportsDate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/stock_reports_date.html',{})

class SalesReturnReport(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            status_code = 200
            start = request.GET['start_date']
            end = request.GET['end_date']            
            start_date = datetime.strptime(start, '%d/%m/%Y')
            end_date = datetime.strptime(end, '%d/%m/%Y')
            salesreturn_report = []
            salesreturn_report_total = []
            grant_total = 0

            salesreturn = SalesReturn.objects.filter(date__gte=start_date,date__lte=end_date)
            
            if salesreturn.count()>0:
                for sale in salesreturn:
                    salesreturn_items = sale.salesreturnitem_set.all()
                    if salesreturn_items.count()>0:
                        for salesreturn_item in salesreturn_items:
                            dates = salesreturn_item.sales_return.date
                            invoice_no = salesreturn_item.sales_return.return_invoice_number
                            qty = salesreturn_item.return_quantity
                            total = salesreturn_item.amount
                            item_name = salesreturn_item.item.item.name
                            item_code = salesreturn_item.item.item.code
                            inventorys = salesreturn_item.item.item.inventory_set.all()[0]
                            unitprice = inventorys.unit_price

                            grant_total = grant_total + total

                            salesreturn_report.append({                        
                                'dates' : dates.strftime('%d-%m-%Y'),
                                'invoice_no' : invoice_no,
                                'qty' : qty,
                                'total' : total,
                                'item_name' : item_name,
                                'item_code' : item_code,                        
                                'unitprice' : unitprice,
                            })
            salesreturn_report_total.append({
                'grant_total' :grant_total,
            })

            try:                
                res = {
                    'result': 'ok',    
                    'salesreturn_report' : salesreturn_report, 
                    'salesreturn_report_total' : salesreturn_report_total,               
                }    
                response = simplejson.dumps(res)
            except Exception as ex:
                response = simplejson.dumps({'result': 'error', 'error': str(ex)})
                status_code = 500
            return HttpResponse(response, status = status_code, mimetype = 'application/json')
        else:
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








