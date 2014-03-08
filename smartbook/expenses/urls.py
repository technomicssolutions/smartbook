from django.conf.urls import patterns, include, url

from expenses.views import *

urlpatterns = patterns('',
	url(r'expenses/$', Expenses.as_view(), name='expenses')

)
