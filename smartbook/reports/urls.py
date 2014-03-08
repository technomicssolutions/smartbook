from django.conf.urls import patterns, include, url

from reports.views import *

urlpatterns = patterns('',
	url(r'reports/$', Reports.as_view(), name='reports'),

)
