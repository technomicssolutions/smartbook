# Create your views here.
from django.db import IntegrityError

from django.contrib.auth.views import password_reset
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Home(View):
    def get(self, request, *args, **kwargs):
        #userprofile=UserProfile.objects.all()
        #context = {'userprofile':userprofile,}
        context = {}
        return render(request, 'home.html',context)
