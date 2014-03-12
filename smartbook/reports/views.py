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
    path = settings.PROJECT_PATH + '/../web/static/img/logo.png'
    p.drawImage(path, 3*cm, 25*cm, width=5*cm, preserveAspectRatio=True)
    p.drawString(x, y, "Sportivore Pty. Ltd.")
    y = 680
    p.drawString(x, y, "ACN  166 877 818")
    y = 660
    p.drawString(x, y, "Phone   +61 424 367 235")
    y = 640
    p.drawString(x, y, "Email   admin@sportivore.com.au")
    data=[['Receipt'],['Date invoiced', str(datetime.now().date())], ['Payment Id', str(response.transaction_response.trans_id)], ['User name', player.user.first_name+' '+player.user.last_name]]
    table = Table(data, colWidths=[100, 215], rowHeights=30)
    table.setStyle(TableStyle([
                               ('INNERGRID', (0,0), (0,0), 0.25, colors.black),
                               ('INNERGRID', (0,1), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('BACKGROUND',(0,0),(1,0),colors.lightgrey)
                               ]))
    table.wrapOn(p, 200, 400)
    table.drawOn(p,85,500)
    game_detail = game.date.strftime('%A, %dth of %B')+ " - " +game.start_time.strftime('%I %p')+' - '+ game.sport.title+ ' at '+ game.court.venue.venue_name
    data=[['Game Details', 'Amount'],[game_detail, game.cost], ['Amount Paid', game.cost]]
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

        if request.is_ajax():
            if request.GET['report_name'] == 'date':
                ctx_purchase_report = []
                status_code = 200
                start_date = request.GET['start_date']
                end_date = request.GET['end_date']
                start_date = datetime.strptime(start_date, '%d/%m/%Y')
                end_date = datetime.strptime(end_date, '%d/%m/%Y')
                purchases = Purchase.objects.filter(purchase_invoice_date__gte=start_date, purchase_invoice_date__lte=end_date).order_by('purchase_invoice_date')
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
                        'amount': purchase.purchaseitem_set.all()[0].net_amount,
                    })
                pdf = createPDF(purchases)
                print pdf
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






