from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

from inventory.models import Item
from inventory.models import Brand
from web.models import Customer, Staff


# Create your models here.   


class Sales(models.Model):	
	sales_invoice_number = models.IntegerField('Sales Invoice Number', default=0)
	sales_invoice_date = models.DateField('Sales Invoice Date', null=True, blank=True)
	customer = models.ForeignKey(Customer, null=True, blank=True)
	salesman = models.ForeignKey(Staff, null=True, blank=True)
	net_amount = models.DecimalField('Net Amount',max_digits=14, decimal_places=3, default=0)
	round_off = models.DecimalField('Net Round Off',max_digits=14, decimal_places=3, default=0)
	grant_total = models.DecimalField('Grand Total',max_digits=14, decimal_places=3, default=0)
	discount = models.DecimalField('Total Discount',max_digits=14, decimal_places=3, default=0)		
	def __unicode__(self):

		return str(self.sales_invoice_number)

	class Meta:

		verbose_name = 'Sales'
		verbose_name_plural = 'Sales'

class SalesItem(models.Model):

	item = models.ForeignKey(Item)
	sales = models.ForeignKey(Sales)
	quantity_sold = models.IntegerField('Quantity Sold', default=0)
	discount_given = models.DecimalField('Discount Given',max_digits=14, decimal_places=3, default=0)	
	
	
	def __unicode__(self):

		return str(self.sales.sales_invoice_number)

	class Meta:

		verbose_name = 'Sales Items'
		verbose_name_plural = 'Sales Items'

class SalesReturn(models.Model):
	sales = models.ForeignKey(Sales)
	return_invoice_number = models.IntegerField('Purchase Return invoice number', unique=True)
	date = models.DateField('Date', null=True, blank=True)
	net_amount = models.IntegerField('Total', null=True, blank=True)
	

	def __unicode__(self):

		return str(self.sales.sales_invoice_number)

class SalesReturnItem(models.Model):
	sales_return = models.ForeignKey(SalesReturn, null=True, blank=True)
	item = models.ForeignKey(SalesItem, null=True, blank=True)
	return_quantity = models.IntegerField('Return Quantity', null=True, blank=True)
	amount = models.IntegerField('Amount', null=True, blank=True)

	def __unicode__(self):

		return str(self.sales.sales_invoice_number)
		


