from django.conf.urls import patterns, include, url

from inventory.views import *

urlpatterns = patterns('',
	url(r'^add_item/$', ItemAdd.as_view(),name='add_item'),

)