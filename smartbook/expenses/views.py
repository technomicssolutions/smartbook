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
from .models import ExpenseHead, Expense

class Expenses(View):
	def get(self, request, *args, **kwargs):
		return render(request, 'expenses/expense.html', {})

class AddExpenseHead(View):

	def get(self, request, *args, **kwargs):

		return render(request, 'expenses/add_expense_head.html', {})

	def post(self, request, *args, **kwargs):

		print request.POST
		post_dict = request.POST

		try:
			if len(post_dict['head_name']) > 0 and not post_dict['head_name'].isspace():
				expense_head, created = ExpenseHead.objects.get_or_create(expense_head = post_dict['head_name'])
				if created:
					context = {
						'message' : 'Added successfully',
					}
				else:
					context = {
						'message' : 'This Head name is Already Existing',
					}
			else:
				context = {
					'message' : 'Head name Cannot be null',
				}
		except Exception as ex:
			print str(ex)
			context = {
				'message' : post_dict['head_name']+' is already existing',
			}
		return render(request, 'expenses/add_expense_head.html', context)


