from django.conf.urls import patterns, include, url

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', Logout.as_view(), name='logout'),
	url(r'^register/(?P<user_type>\w+)/$', RegisterUser.as_view(), name='register_user'),
	url(r'^(?P<user_type>\w+)/list/$', UserList.as_view(), name='users'),	
)