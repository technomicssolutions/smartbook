from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from inventory.models import Item
from inventory.models import Brand
from web.models import Vendor, TransportationCompany

# Create your models here.   


class Purchase(models.Model):
	
	purchase_invoice_number = models.IntegerField('Purchase Invoice Number', unique=True)
	vendor_invoice_number = models.IntegerField('Vendor Invoice Number', default=0)
	vendor_do_number = models.IntegerField('Vendor DO Number', default=0)
	vendor_invoice_date = models.DateField('Vendor Invoice Date', null=True, blank=True)
	purchase_invoice_date = models.DateField('Purchase Invoice Date', null=True, blank=True)
	brand = models.ForeignKey(Brand, null=True, blank=True)
	vendor = models.ForeignKey(Vendor, null=True, blank=True)
	transportation_company = models.ForeignKey(TransportationCompany, null=True, blank=True)
	discount = models.DecimalField('Discount',max_digits=14, decimal_places=3, default=0)
	
	
	def __unicode__(self):
		return str(self.purchase_invoice_number)

	class Meta:

		verbose_name = 'Purchase'
		verbose_name_plural = 'Purchase'

class PurchaseItem(models.Model):

	item = models.ForeignKey(Item, null=True, blank=True)
	purchase = models.ForeignKey(Purchase, null=True, blank=True)
	item_frieght = models.IntegerField('Item Frieght', default=0)
	frieght_per_unit = models.IntegerField('Item Frieght per Unit', default=0)
	item_handling = models.IntegerField('Item Handling', default=0)
	handling_per_unit = models.IntegerField('Item Handling per Unit', default=0)
	expense = models.IntegerField('Expense', default=0)
	expense_per_unit = models.IntegerField('Expense per Unit', default=0)
	net_amount = models.DecimalField('Net Amount',max_digits=14, decimal_places=3, default=0)
	vendor_amount = models.DecimalField('Vendor Amount',max_digits=14, decimal_places=3, default=0)
	quantity_purchased = models.IntegerField('Quantity Purchased', default=0)
	cost_price = models.DecimalField('Cost Price',max_digits=14, decimal_places=3, default=0)


	def __unicode__(self):

		return self.purchase.purchase_invoice_number

	class Meta:

		verbose_name = 'Purchase Items'
		verbose_name_plural = 'Purchase Items'


class PurchaseReturn(models.Model):
	purchase = models.ForeignKey(Purchase)
	date = models.DateField('Date')
	time = models.TimeField('Time')
	quantity = models.IntegerField('Quantity')

	def __unicode__(self):
		return self.purchase
