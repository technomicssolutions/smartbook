from django.contrib import admin
from purchase.models import *



admin.site.register(Purchase)
admin.site.register(ExpenseType)
admin.site.register(PurchaseTxpense)
admin.site.register(PurchaseReturn)

