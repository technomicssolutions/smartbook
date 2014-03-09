from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

USER_TYPE = (
	('vendor', 'Vendor'),
	('customer', 'Customer'),
	('staff','Staff')
)

class Designation(models.Model):

	title = models.CharField('Designation title', max_length=50)
	description = models.CharField('Description', max_length=100, null=True, blank=True)

	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	user_type = models.CharField('User Type', max_length=10, choices=USER_TYPE)
	house_name = models.CharField('House name', null=True, blank=True, max_length=15)
	street = models.CharField('Street', null=True, blank=True, max_length=10)
	city = models.CharField('City', null=True, blank=True, max_length=10)
	district = models.CharField('District', null=True, blank=True, max_length=10)
	pin = models.CharField('Pin', max_length=10, null=True, blank=True,)
	mobile = models.CharField('Mobile', max_length=10, null=True, blank=True)
	land_line = models.CharField('Land Line',max_length=10, blank=True)
	email_id = models.CharField('Email Id', max_length=25)

	def __unicode__(self):
		return self.user.username

class Vendor(models.Model):
	user = models.ForeignKey(User)
	contact_person = models.CharField('Contact Person', max_length=10)	

	def __unicode__(self):
		return "vendor - ", self.user.userprofile.user.first_name

	
class Customer(models.Model):
	user = models.ForeignKey(User)

	def __unicode__(self):
		return "customer - ", self.user.userprofile.user.first_name

		
class Staff(models.Model):
	user = models.ForeignKey(User)
	designation = models.ForeignKey(Designation, null=True, blank=True)

	def __unicode__(self):
		return "staff - ", self.user.userprofile.user.first_name
			