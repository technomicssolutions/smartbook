from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ExpenseHead(models.Model):
	expense_head = models.CharField('Expense Head', max_length=15, unique=True)

	class Meta:
		verbose_name = 'Expense Head'
		verbose_name_plural = 'Expense Head'

	def __unicode__(self):

		return self.expense_head

class  Expense(models.Model):
	created_by = models.ForeignKey(User)

	expense_head = models.ForeignKey(ExpenseHead)
	voucher_no = models.IntegerField('Voucher No')
	date = models.DateField('Date')
	amount = models.IntegerField('Amount')
	payment_mode = models.BooleanField('Payment Mode', default=False)
	narration = models.TextField('Narration', max_length=300, null=True, blank=True)
	
	cheque_no = models.IntegerField('Cheque No')
	cheque_date = models.DateField('Cheque Date')
	bank_name = models.CharField('Bank Name', max_length=15)
	branch = models.CharField('Branch', max_length=10)

	class Meta:
		verbose_name = 'Expense'
		verbose_name_plural = 'Expense'

	def __unicode__(self):

		return self.voucher_no

