from django.db import models
from datetime import datetime
from inventory.models import Item
from inventory.models import Brand
from django.contrib.auth.models import User

# Create your models here.   


class Purchase(models.Model):
	invoice_number = models.IntegerField('Invoice Number')
	item = models.ForeignKey(Item)
	brand = models.ForeignKey(Brand)
	vendor = models.ForeignKey(User)
	date = models.DateField('Date')
	time = models.TimeField('Time')
	quantity = models.IntegerField('Quantity')
	cost_price = models.DecimalField('Cost Price',max_digits=14, decimal_places=2, default=0)
	selling_price = models.DecimalField('Selling Price',max_digits=14, decimal_places=2, default=0)
	
	
	def __unicode__(self):
		return self.invoice_number


class Expense_type(models.Model):
	category = models.CharField("Type",max_digits=14) 

	def __unicode__(self):
		return self.category


class Purchase_expense(models.Model):
	purchase = models.ForeignKey(Purchase)
	category = models.ForeignKey(Expense_type)
	total = models.DecimalField('Total Amout',max_digits=14, decimal_places=2, default=0)
	paid = models.DecimalField('Paid Amout',max_digits=14, decimal_places=2, default=0)

	def __unicode__(self):
		return self.purchase


class Purchase_return(models.Model):
	purchase = models.ForeignKey(Purchase)
	date = models.DateField('Date')
	time = models.TimeField('Time')
	quantity = models.IntegerField('Quantity')

	def __unicode__(self):
		return self.purchase
