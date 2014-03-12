import sys
import ast
import simplejson
import datetime as dt
from datetime import datetime

from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Max

from inventory.models import Item
from inventory.models import UnitOfMeasure
from inventory.models import Brand

from web.models import (UserProfile, Vendor, Customer, Staff, TransportationCompany)
from purchase.models import Purchase, PurchaseItem, VendorAccount
from inventory.models import Inventory
from expenses.models import Expense, ExpenseHead

class PurchaseDetail(View):

    def get(self, request, *args, **kwargs):
        try:
            invoice_number = request.GET.get('invoice_no', '')
            purchase  = Purchase.objects.get(purchase_invoice_number=int(invoice_number))
            purchase_items = PurchaseItem.objects.filter(purchase=purchase)
            items_list = []
            for item in purchase_items:
                items_list.append({
                    'item_code': item.item.code,
                    'item_name': item.item.name,
                    'barcode': item.item.barcode,
                    'uom': item.item.uom.uom,
                    'current_stock': item.item.inventory_set.all()[0].quantity,
                    'frieght': item.item_frieght,
                    'frieght_unit': item.frieght_per_unit,
                    'handling': item.item_handling,
                    'handling_unit': item.handling_per_unit,                
                    'selling_price': item.item.inventory_set.all()[0].selling_price,
                    'qty_purchased': item.quantity_purchased,
                    'cost_price': item.cost_price,
                    'permit_disc_amt': item.item.inventory_set.all()[0].discount_permit_amount,
                    'permit_disc_percent': item.item.inventory_set.all()[0].discount_permit_percentage,
                    'net_amount': item.net_amount,
                    'unit_price': item.item.inventory_set.all()[0].unit_price,
                    'expense': item.expense,
                    'expense_unit': item.expense_per_unit,
                })

            purchase_dict = {
                'purchase_invoice_number': purchase.purchase_invoice_number,
                'vendor_invoice_number': purchase.vendor_invoice_number,
                'vendor_do_number': purchase.vendor_do_number,
                'brand': purchase.brand.brand,
                'vendor': purchase.vendor.user.first_name,
                'transport': purchase.transportation_company.company_name,
                'vendor_invoice_date': purchase.vendor_invoice_date.strftime('%d/%m/%Y'),
                'purchase_invoice_date': purchase.purchase_invoice_date.strftime('%d/%m/%Y'), 
                'purchase_items': items_list,
                'vendor_amount': purchase.vendor_amount,
                'net_total': purchase.net_total,
                'purchase_expense': purchase.purchase_expense,
                'discount': purchase.discount,
                'grant_total': purchase.grant_total    
            }
            res = {
                'result': 'Ok',
                'purchase': purchase_dict
            } 
            response = simplejson.dumps(res)
            status_code = 200
        except Exception as ex:
            res = {
                'result': 'No item with this purchase NO'+ str(ex),
                'purchase': {}
            } 
            response = simplejson.dumps(res)
            status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class PurchaseEntry(View):

    def get(self, request, *args, **kwargs):
    	brand = Brand.objects.all()
    	vendor = Vendor.objects.all()
        transport = TransportationCompany.objects.all()
        if Purchase.objects.exists():
            invoice_number = int(Purchase.objects.aggregate(Max('purchase_invoice_number'))['purchase_invoice_number__max']) + 1
        else:
            invoice_number = 1
        if not invoice_number:
            invoice_number = 1
        return render(request, 'purchase/purchase_entry.html',{
        	'invoice_number': invoice_number,
    	})

    def post(self, request, *args, **kwargs):

        purchase_dict = ast.literal_eval(request.POST['purchase'])
        purchase, purchase_created = Purchase.objects.get_or_create(purchase_invoice_number=1)
        purchase.purchase_invoice_number = purchase_dict['purchase_invoice_number']
        purchase.vendor_invoice_number = purchase_dict['vendor_invoice_number']
        purchase.vendor_do_number = purchase_dict['vendor_do_number']
        purchase.vendor_invoice_date = datetime.strptime(purchase_dict['vendor_invoice_date'], '%d/%m/%Y')
        purchase.purchase_invoice_date = datetime.strptime(purchase_dict['purchase_invoice_date'], '%d/%m/%Y')
        brand = Brand.objects.get(brand=purchase_dict['brand'])
        purchase.brand = brand
        vendor = Vendor.objects.get(user__first_name=purchase_dict['vendor'])       
        transport = TransportationCompany.objects.get(company_name=purchase_dict['transport'])
        purchase.vendor = vendor
        purchase.transportation_company = transport
        purchase.discount = purchase_dict['discount']
        purchase.net_total = purchase_dict['net_total']
        purchase.purchase_expense = purchase_dict['purchase_expense']
        purchase.grant_total = purchase_dict['grant_total']

        vendor_account, vendor_account_created = VendorAccount.objects.get_or_create(vendor=vendor)
        if vendor_account_created:
            vendor_account.total_amount = purchase.vendor_amount
            vendor_account.balance = purchase.vendor_amount
        else:
            if purchase_created:
                vendor_account.total_amount = vendor_account.total_amount + purchase_dict['vendor_amount']
                vendor_account.balance = vendor_account.balance + purchase_dict['vendor_amount']
            else:
                vendor_account.total_amount = vendor_account.total_amount - purchase.vendor_amount + purchase_dict['vendor_amount']
                vendor_account.balance = vendor_account.balance - purchase.vendor_amount + purchase_dict['vendor_amount']
        vendor_account.save()       
        purchase.vendor_amount = purchase_dict['vendor_amount']
        purchase.save()

        

        # Save purchase_expense in Expense
        if Expense.objects.exists():
            voucher_no = int(Expense.objects.aggregate(Max('voucher_no'))['voucher_no__max']) + 1
        else:
            voucher_no = 1
        if not voucher_no:
            voucher_no = 1
        expense = Expense()
        expense.created_by = request.user
        expense.expense_head, created = ExpenseHead.objects.get_or_create(expense_head = 'purchase')
        expense.date = dt.datetime.now().date().strftime('%Y-%m-%d')
        expense.voucher_no = voucher_no
        expense.amount = purchase_dict['purchase_expense']
        expense.payment_mode = 'cash'
        expense.narration = 'By purchase'
        expense.save()

        

        purchase_items = purchase_dict['purchase_items']
        deleted_items = purchase_dict['deleted_items']

        for p_item in deleted_items:
            item = Item.objects.get(code = p_item['item_code']) 
            ps_item = PurchaseItem.objects.get(item=item)           
            inventory = Inventory.objects.get(item=item)
            inventory.quantity = inventory.quantity + ps_item.quantity_purchased
            inventory.save()
            ps_item.delete()

        for purchase_item in purchase_items:

            item = Item.objects.get(code=purchase_item['item_code'])
            p_item, item_created = PurchaseItem.objects.get_or_create(item=item, purchase=purchase)
            inventory, created = Inventory.objects.get_or_create(item=item)
            if created:
                inventory.quantity = int(purchase_item['qty_purchased'])                
            else:
                if purchase_created:
                    inventory.quantity = inventory.quantity + int(purchase_item['qty_purchased'])
                else:
                    inventory.quantity = inventory.quantity - p_item.quantity_purchased + int(purchase_item['qty_purchased'])
            inventory.selling_price = purchase_item['selling_price']
            inventory.unit_price = purchase_item['unit_price']
            inventory.discount_permit_percentage = purchase_item['permit_disc_percent']
            inventory.discount_permit_amount = purchase_item['permit_disc_amt']
            inventory.save()  
                    
            p_item, item_created = PurchaseItem.objects.get_or_create(item=item, purchase=purchase)
            p_item.purchase = purchase
            p_item.item = item
            p_item.quantity_purchased = purchase_item['qty_purchased']
            p_item.item_frieght = purchase_item['frieght']
            p_item.frieght_per_unit = purchase_item['frieght_unit']
            p_item.item_handling = purchase_item['handling']
            p_item.handling_per_unit = purchase_item['handling_unit']
            p_item.expense = purchase_item['expense']
            p_item.expense_per_unit = purchase_item['expense_unit']
            p_item.cost_price = purchase_item['cost_price']
            p_item.net_amount = purchase_item['net_amount']
            p_item.save()
                    
        res = {
            'result': 'Ok',
        } 

        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")


class PurchaseEdit(View):
    def get(self, request, *args, **kwargs):
    	
        return render(request, 'purchase/edit_purchase_entry.html',{})

class VendorAccounts(View):
    def get(self, request, *args, **kwargs):
        vendor_accounts =  VendorAccount.objects.all()
        return render(request, 'purchase/vendor_accounts.html', {
            'vendor_accounts' : vendor_accounts
        })
        

class VendorAccountDetails(View):
    def get(self, request, *args, **kwargs):
        vendor = Vendor.objects.get_object_or_404(user__first_name=kwargs['vendor'])
        vendor_account =  VendorAccount.objects.get(vendor=vendor)
        return render(request, 'purchase/vendor_accounts.html', {
            'vendor_accounts' : vendor_account
        })
        