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


from django.db import IntegrityError

from web.models import (UserProfile, Vendor, Customer, Staff, Designation)


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

class UserList(View):
    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        if user_type == 'staff':
            users = UserProfile.objects.filter(user_type='staff')
        elif user_type == 'vendor':
            users = UserProfile.objects.filter(user_type='vendor')
        elif user_type == 'customer':
            users = UserProfile.objects.filter(user_type='customer')
        return render(request, 'user_list.html',{
            'users': users,
            'user_type': user_type
        })

class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        user_type = kwargs['user_type']
        if user_type == 'vendor':
            return render(request, 'add_vendor.html',{})
        elif user_type == 'staff':
            designations = Designation.objects.all()
            return render(request, 'add_staff.html',{'designations': designations})
        elif user_type == 'customer':
            return render(request, 'add_customer.html',{})


    def post(self, request, *args, **kwargs):

        userprofile = UserProfile()
        context={}
        user_type = kwargs['user_type']
        try:
            user = User.objects.create(username=request.POST['name'], email = request.POST['email'])
            user.save()
            userprofile.user_type="vendor"
            userprofile.user = user
            userprofile.house_name =request.POST['house']
            userprofile.street = request.POST['street']
            userprofile.city = request.POST['city']
            userprofile.district = request.POST['district']
            userprofile.pin = request.POST['pin']
            userprofile.mobile = request.POST['mobile']
            userprofile.land_line = request.POST['phone']
            userprofile.email_id = request.POST['email']
            userprofile.save()
            if user_type == 'vendor':
                vendor = Vendor()  
                vendor.contact_person= request.POST['contact']
                vendor.user = user
                vendor.save()
                context = {
                    'message' : 'Vendor added correctly',
                }
                return render(request, 'add_vendor.html',context)
            elif user_type == 'staff':
                staff = Staff()
                staff.designation = request.POST['designation']
                staff.save()
                context = {
                    'message' : 'Staff added correctly',
                }
                return render(request, 'add_staff.html',context)
            elif user_type == 'customer':
                context = {
                    'message' : 'Customer Added Successfully',
                }
                return render(request, 'add_customer.html', context)
        
        except IntegrityError:
            message = ''
            if user_type == 'vendor':
                message = 'Vendor with this name already exists'
            elif user_type == 'staff':
                message = 'Staff with this name already exists'
            elif user_type == 'customer':
                message = 'Cuatomer with this name already exists'
            context = {
                'error_message': message
            }
            context.update(request.POST)
            return render(request, 'add_customer.html', context)
        

class StaffList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_staff.html',{})



class CustomerList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'list_customer.html',{})









