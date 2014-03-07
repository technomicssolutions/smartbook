from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Uom(models.Model):
	uom = models.CharField('Unit Of Measure', max_length=50)
	def __unicode__(self):
		return self.uom
        

class Brand(models.Model):
	name = models.CharField('Brand', max_length=50)
	description= models.CharField('Brand', max_length=50)
	
	def __unicode__(self):
		return self.name


class Item(models.Model):

	code = models.IntegerField('Item Code')
	name = models.CharField('Name', max_length=50)
	brand = models.ForeignKey(Brand)
	description = models.TextField('Description', max_length=50)
	vendor = models.ForeignKey(User)
	uom = models.ForeignKey(Uom)
	barcode = models.CharField('Barcode', max_length=50)
	tax = models.DecimalField('Tax',max_digits=14, decimal_places=2, default=0)
	def __unicode__(self):
		return self.code


class Inventory(models.Model):
	item = models.ForeignKey(Item)
	quantity = models.IntegerField('Quantity')
	unit_price = models.DecimalField('Unit Price',max_digits=14, decimal_places=2, default=0)
	selling_price = models.DecimalField('Selling Price',max_digits=14, decimal_places=2, default=0)


	def __unicode__(self):
		return self.item