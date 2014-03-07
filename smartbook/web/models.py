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
	user_type = models.CharField('User Type', max_length=10, choices=USER_TYPE)
	house_name = models.CharField('House name', null=True, blank=True, max_length=15)
	street = models.CharField('Street', null=True, blank=True, max_length=10)
	city = models.CharField('City', null=True, blank=True, max_length=10)
	district = models.CharField('District', null=True, blank=True, max_length=10)
	pin = models.IntegerField('Pin', null=True, blank=True,)
	mobile = models.IntegerField('Mobile')
	land_line = models.IntegerField('Land Line', blank=True)
	email_id = models.CharField('Email Id', max_length=25)

	def __unicode__(self):
		return self.user.Username

class Vendor(models.Model):
	userprofile = models.ForeignKey(User)
	contact_person = models.CharField('Contact Person', max_length=10)	

	def __unicode__(self):
		return "vendor" + self.user.userprofile.user.firstname

	
class Customer(models.Model):
	userprofile = models.ForeignKey(User)

	def __unicode__(self):
		return "customer" + self.user.userprofile.user.firstname

		
class Staff(models.Model):
	userprofile = models.ForeignKey(User)
	designation = models.CharField('Designation', max_length=10)

	def __unicode__(self):
		return "staff" + self.user.userprofile.user.firstname
			