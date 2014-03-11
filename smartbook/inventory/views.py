import sys
import simplejson

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
        #try:
        item_code = request.GET.get('item_code', '')
        item_name = request.GET.get('item_name', '')
        barcode = request.GET.get('barcode', '')
        items = []
        if item_code:
            items = Item.objects.filter(code__istartswith=item_code)
        elif item_name:
            items = Item.objects.filter(name__istartswith=item_name)
        elif barcode:
            items = Item.objects.filter(barcode__istartswith=barcode)
        item_list = []
        for item in items:
            item_list.append({
                'item_code': item.code,
                'item_name': item.name,
                'barcode': item.barcode,
                'brand': item.brand.brand,
                'tax': item.tax,
                'uom': item.uom.uom,
                'current_stock': item.inventory_set.all()[0].quantity if item.inventory_set.count() > 0  else 0 ,
                'selling_price': item.inventory_set.all()[0].selling_price if item.inventory_set.count() > 0 else 0 ,
                'discount_permit': item.inventory_set.all()[0].discount_permit if item.inventory_set.count >0 else 0,
            })

        res = {
            'items': item_list,
        }
        response = simplejson.dumps(res)

        # except Exception as ex:
        #     response = simplejson.dumps({'result': 'error', 'error': str(ex)})
        #     status_code = 500
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype = 'application/json')


class ItemEdit(View):
    def get(self, request, *args, **kwargs):
        items = Item.objects.get(id = kwargs['item_id'])
        brand = Brand.objects.all()
        uom = UnitOfMeasure.objects.all()
        ctx ={
            'items':items,
            'uoms': uom,
            'brands': brand,
        }
        return render(request, 'inventory/edit_item.html',ctx)

class Itemdelete(View):
    def get(self, request, *args, **kwargs):
        message =""
        try:
            items = Item.objects.get(id = kwargs['item_id']).delete()
        except:
            message = "already deleted"
        items = Item.objects.all()
        return render(request, 'inventory/item_list.html',{
            'items':items,
            'message':message,
        })

class UpdateItem(View):
    def post(self, request, *args, **kwargs):
        item = Item.objects.get(id = request.POST['id'])
        item.code = request.POST['code']
        item.name =request.POST['name']
        item.description =request.POST['description']
        item.tax =request.POST['tax']
        brand =Brand.objects.get(brand=request.POST['brand'])
        item.brand=brand
        uom =UnitOfMeasure.objects.get(uom=request.POST['uom'])
        item.uom=uom
        item.save()
        items = Item.objects.all()
        return render(request, 'inventory/item_list.html',{
            'items':items,
        })


