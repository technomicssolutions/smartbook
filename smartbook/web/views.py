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

from web.models import (UserProfile,Vendor,Customer,Staff)


class Home(View):
    def get(self, request, *args, **kwargs):
        #userprofile=UserProfile.objects.all()
        #context = {'userprofile':userprofile,}
        context = {}
        return render(request, 'home.html',context)

class Login(View):

    def post(self, request, *args, **kwargs):

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user and user.is_active:
            login(request, user)
        else:
            context = {
                'message' : 'Username or password is incorrect'
            }
            return render(request, 'home.html',context)
        return HttpResponseRedirect(reverse('home'))

class Logout(View):

    def get(self, request, *args, **kwargs):

        logout(request)
        return HttpResponseRedirect(reverse('home'))

class VendorList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_vendor.html',{})

class VendorAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add_vendor.html',{})

    def post(self, request, *args, **kwargs):
        user = User()
        userprofile = UserProfile()
        vendor = Vendor()
        context={}
        try:
            user.username=request.POST['name']
            user.save()
            print "2222",request.POST['house']
            userprofile.user_type="vendor"
            userprofile.house_name =request.POST['house']
            userprofile.street = request.POST['street']
            userprofile.city = request.POST['city']
            userprofile.district = request.POST['district']
            userprofile.pin = request.POST['pin']
            userprofile.mobile = request.POST['mobile']
            userprofile.land_line = request.POST['phone']
            userprofile.email_id = request.POST['email']
            userprofile.save()
            vendor.contact_person= request.POST['contact']
            vendor.save()
            context = {
                    'message' : 'Vendor added correctly',
                }
        except:
            print "Unexpected error:", sys.exc_info()[0]
        return render(request, 'add_vendor.html',context)

class StaffList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_vendor.html',{})

class StaffAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_vendor.html',{})

class CustomerList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_vendor.html',{})

class CustomerAdd(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_vendor.html',{})








