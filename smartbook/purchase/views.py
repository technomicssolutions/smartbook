import sys

from django.db import IntegrityError

from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from inventory.models import Item
from inventory.models import UnitOfMeasure
from inventory.models import Brand

from web.models import (UserProfile,Vendor,Customer,Staff)

class PurchaseEntry(View):
    def get(self, request, *args, **kwargs):
    	brand = Brand.objects.all()
    	vendor = Vendor.objects.all()

        return render(request, 'purchase/purchase_entry.html',{
        	'brands' : brand,
        	'vendors' : vendor,
        	})
class PurchaseEdit(View):
    def get(self, request, *args, **kwargs):
    	
        return render(request, 'purchase/edit_purchase_entry.html',{
        	
        	})

