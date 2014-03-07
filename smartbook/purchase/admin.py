from django.contrib import admin
from purchase.models import *



admin.site.register(Purchase)
admin.site.register(Expense_type)
admin.site.register(Purchase_expense)
admin.site.register(Purchase_return)

