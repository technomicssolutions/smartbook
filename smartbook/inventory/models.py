from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UnitOfMeasure(models.Model):
	uom = models.CharField('Unit Of Measure', max_length=50, unique=True)
	def __unicode__(self):
		return self.uom
        

class Brand(models.Model):
	brand = models.CharField('Brand', max_length=51, unique=True)
	
	
	def __unicode__(self):
		return self.brand


class Item(models.Model):

	code = models.CharField('Item Code', max_length=10)
	name = models.CharField('Name', max_length=50)
	description = models.TextField('Description', max_length=50,null=True, blank=True)
	uom = models.ForeignKey(UnitOfMeasure)
	brand = models.ForeignKey(Brand)
	barcode = models.CharField('Barcode', max_length=50,null=True, blank=True)
	tax = models.DecimalField('Tax',max_digits=14, decimal_places=2, default=0)
	def __unicode__(self):
		return self.code


class Inventory(models.Model):
	item = models.ForeignKey(Item)
	quantity = models.IntegerField('Quantity')
	unit_price = models.DecimalField('Unit Price',max_digits=14, decimal_places=2, default=0)
	selling_price = models.DecimalField('Selling Price',max_digits=14, decimal_places=2, default=0)
	discount_permit = models.DecimalField('Allowed Discount',max_digits=14, decimal_places=2, default=0,null=True, blank=True)

	def __unicode__(self):
		return self.item.code