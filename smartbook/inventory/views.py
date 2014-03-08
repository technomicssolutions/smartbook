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

class ItemAdd(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'inventory/new_item.html',{})# Create your views here.

	def post(self, request, *args, **kwargs):
              
		item_add= Item()
		uom_add = UnitOfMeasure()
		
		context={}
		try:
            
			item_add.code =request.POST['code']
			item_add.name =request.POST['name']
			item_add.description =request.POST['description']
			uom=UnitOfMeasure.objects.get(uom=request.POST['add_uom'])
			uom_add.uom = uom
			uom_add.save()
			item_add.barcode =request.POST['barcode']
			item_add.tax =request.POST['tax']
			item_add.save()

			context = {
				'message' : 'Item Addes Successfully.',
                }
		except:
			print "Unexpected error:", sys.exc_info()[0]
		return render(request, 'inventory/new_item.html',context)
