from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

USER_TYPE = (
	('vendor', 'Vendor'),
	('customer', 'Customer'),
	('staff','Staff')
)

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	user_type = models.CharField('User Type', max_length=10)
	vendor_id = models.IntegerField('Vendor Id')
	contact_person = models.CharField('Contact Person', max_length=15)
	address = models.CharField('Address', max_length=30)
	contact_no = models.IntegerField('Contact No')
	email = models.CharField('Email', max_length=25)

class Customer(models.Model):
	user = models.ForeignKey(User)
	customer_id = models.IntegerField('Customer Id')
	cutomer_name = models.CharField('Customer Name', max_length=10)
	house_name = models.CharField('House name', max_length=15)
	street = models.CharField('Street', max_length=10)
	city = models.CharField('City', max_length=10)
	district = models.CharField('District', max_length=10)
	pin = models.IntegerField('Pin')
	mobile = models.IntegerField('Mobile')
	land_line = models.IntegerField('Land Line', blank=True)
	email_id = models.CharField('Email Id', max_length=25)

class Staff(models.Model):
	user = models.ForeignKey(User)
	salesman_id = models.IntegerField('Salesman Id')
	salesman_name = models.CharField('Salesman Name', max_length=10)
	address = models.CharField('Address', max_length=30)
	mobile = models.IntegerField('Mobile')
	land_line = models.IntegerField('Land Line', blank=True)
	
class Designation(models.Model):
	user = models.ForeignKey(User)
	designation = models.CharField('Designation', max_length=10)



# Create your models here.
