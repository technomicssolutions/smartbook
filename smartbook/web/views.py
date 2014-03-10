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
            return render(request, 'register_user.html',{'user_type': user_type})
        elif user_type == 'staff':
            designations = Designation.objects.all()
            return render(request, 'register_user.html',{
                'designations': designations,
                'user_type': user_type
            })
        elif user_type == 'customer':
            return render(request, 'register_user.html',{'user_type': user_type})


    def post(self, request, *args, **kwargs):
        
        userprofile = UserProfile()
        context={}
        user_type = kwargs['user_type']
        
        user, created = User.objects.get_or_create(username=request.POST['name']+user_type, first_name = request.POST['name'])
        if not created:
            message = ''
            template = 'register_user.html'
            if user_type == 'vendor':
                message = 'Vendor with this name already exists'
            elif user_type == 'staff':
                message = 'Staff with this name already exists'
            elif user_type == 'customer':
                message = 'Customer with this name already exists'
            context = {
                'error_message': message,
                'user_type': user_type
            }
            context.update(request.POST)
            return render(request, template, context)
        else:
            user.email = request.POST['email']
            user.save()
        userprofile.user_type=user_type
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
                'user_type': user_type
            }
            return render(request, 'register_user.html',context)
        elif user_type == 'staff':
            staff = Staff()
            staff.designation = request.POST['designation']
            staff.save()
            context = {
                'message' : 'Staff added correctly',
                'user_type': user_type
            }
            return render(request, 'register_user.html',context)
        elif user_type == 'customer':
            context = {
                'message' : 'Customer Added Successfully',
                'user_type': user_type
            }
            return render(request, 'register_user.html', context)
    
        
# class UsersListView(View):

#     def get(self, request, *args, *kwargs):

        









