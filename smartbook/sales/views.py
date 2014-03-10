# Create your views here.
import sys

from django.db import IntegrityError

from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

#from sales.models import *

class Sales(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sales/sales_entry.html',{})

class SalesReturn(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sales/sales_return.html',{})

class ViewSales(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sales/view_sales.html',{})

