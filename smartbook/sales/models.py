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
		return self.customer.user.first_name

	class Meta:

		verbose_name = 'Sales'
		verbose_name_plural = 'Sales'

class SalesItem(models.Model):

	item = models.ForeignKey(Item, null=True, blank=True)
	sales = models.ForeignKey(Sales, null=True, blank=True)
	quantity_sold = models.IntegerField('Quantity Sold', default=0)
	discount_given = models.DecimalField('Discount Given',max_digits=14, decimal_places=3, default=0)	
	
	
	def __unicode__(self):

		return self.sales.customer.user.first_name


	class Meta:

		verbose_name = 'Sales Items'
		verbose_name_plural = 'Sales Items'


