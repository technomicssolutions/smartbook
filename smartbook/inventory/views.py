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

class ItemAdd(View):
	def get(self, request, *args, **kwargs):
		uom = UnitOfMeasure.objects.all()
		brand = Brand.objects.all()
		return render(request, 'inventory/new_item.html',{
			'uoms': uom,
			'brands': brand ,
		})# Create your views here.

	def post(self, request, *args, **kwargs):
              
		item_add= Item()
		uom_add = UnitOfMeasure()
		brand_add = Brand()
		
		context={}
		            
		item_add.code =request.POST['code']
		item_add.name =request.POST['name']
		item_add.description =request.POST['description']
		uom =UnitOfMeasure.objects.get(uom=request.POST['uom'])
		brand =Brand.objects.get(brand=request.POST['brand'])
		item_add.barcode =request.POST['barcode']
		item_add.tax =request.POST['tax']
		item_add.brand=brand
		item_add.uom=uom
		item_add.save()
		brand = Brand.objects.all()
		uom = UnitOfMeasure.objects.all()
		return render(request, 'inventory/new_item.html',{
			'uoms': uom,
			'brands': brand,
		})


class ItemList(View):
	def get(self, request, *args, **kwargs):
		items = Item.objects.all()
		ctx = {
			'items':items,
		}
		return render(request, 'inventory/item_list.html',ctx)


class ItemEdit(View):
	def get(self, request, *args, **kwargs):
		print "item ",kwargs['item_id']
		items = Item.objects.get(id = kwargs['item_id'])
		print "items",items.name
		ctx ={
			'items':items,
		}
		return render(request, 'inventory/edit_item.html',ctx)


