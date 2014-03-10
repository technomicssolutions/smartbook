# Create your views here.

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
            return render(request, 'register_user.html',{
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
            vendor.contact_person= request.POST['contact_person']
            vendor.user = user
            vendor.save()
            context = {
                'message' : 'Vendor added correctly',
                'user_type': user_type
            }
            return render(request, 'register_user.html',context)
        elif user_type == 'staff':
            designation = Designation.objects.get(title=request.POST['designation'])
            staff = Staff()
            staff.designation = designation
            staff.user = user
            staff.save()
            context = {
                'message' : 'Staff added correctly',
                'user_type': user_type
            }
            return render(request, 'register_user.html',context)
        elif user_type == 'customer':
            customer = Customer()
            customer.user = user
            customer.save()
            context = {
                'message' : 'Customer Added Successfully',
                'user_type': user_type
            }
            return render(request, 'register_user.html', context)
    
        
class EditUser(View):

    def get(self, request, *args, **kwargs):

        user_type = kwargs['user_type']
        userprofile = UserProfile.objects.get(id=kwargs['profile_id'])
        if user_type == 'vendor':
            return render(request, 'edit_user.html',{'user_type': user_type, 'profile': userprofile})
        elif user_type == 'staff':
            return render(request, 'edit_user.html',{
                'user_type': user_type,
                'profile': userprofile

            })
        elif user_type == 'customer':
            return render(request, 'edit_user.html',{'user_type': user_type,'profile': userprofile})

    def post(self, request, *args, **kwargs):

        user_type = kwargs['user_type']
        userprofile = UserProfile.objects.get(id=kwargs['profile_id'])
        post_dict = request.POST
        user = userprofile.user
        user.first_name = post_dict['name']
        user.username= post_dict['name']+user_type
        user.email = post_dict['email']
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
            vendor = user.vendor_set.all()[0]  
            vendor.contact_person= request.POST['contact_person']
            vendor.user = user
            vendor.save()
            context = {
                'message' : 'Vendor edited correctly',
                'user_type': user_type,
                'profile': userprofile
            }
            return render(request, 'edit_user.html',context)
        if user_type == 'customer':
            customer = user.customer_set.all()[0]
            customer.user = user
            customer.save()
            context = {
                'message' : 'Customer edited correctly',
                'user_type': user_type,
                'profile': userprofile
            }
            return render(request, 'edit_user.html',context)

class DesignationList(View):

    def get(self, request, *args, **kwargs):

        ctx = []
        designations = Designation.objects.all()
        if designations.count() > 0:
            for designation in designations:
                ctx.append({
                    'title':designation.title,    
                })
        res = {
            'designations': ctx,
        } 
        response = simplejson.dumps(res)
        status_code = 200
        return HttpResponse(response, status = status_code, mimetype="application/json")

class AddDesignation(View):

    def post(self, request, *args, **kwargs):

        designation, created = Designation.objects.get_or_create(title=request.POST['new_designation']) 
        if not created:
            res = {
                'result': 'error',
                'message': 'Designation Already exists'
            }
        else:
            res = {
                'result': 'ok',
                'designation': designation.title
            }
        response = simplejson.dumps(res)
        return HttpResponse(response, status=200, mimetype='application/json')











