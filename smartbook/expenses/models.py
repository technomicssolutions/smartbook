from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ExpenseHead(models.Model):
	expense_head = models.CharField('Expense Head', max_length=15)

class  Expense(models.Model):
	created_by = models.ForeignKey(User)
	expense_head = models.ForeignKey(ExpenseHead)
	voucher_no = models.IntegerField('Voucher No')
	date = models.DateField('Date')
	head = models.CharField('Head', max_length=15)
	amount = models.IntegerField('Amount')
	pay_mode = models.CharField('Payment Mode', max_length=8)
	
	cheque_no = models.IntegerField('Cheque No')
	cheque_date = models.DateField('Cheque Date')
	bank_name = models.CharField('Bank Name', max_length=15)
	branch = models.CharField('Branch', max_length=10)

