from django.conf.urls import patterns, include, url

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', Logout.as_view(), name='logout'),
	url(r'^register/(?P<user_type>\w+)/$', RegisterUser.as_view(), name='register_user'),
	url(r'^(?P<user_type>\w+)/list/$', UserList.as_view(), name='users'),
	url(r'^(?P<user_type>\w+)/(?P<profile_id>\d+)/edit/$', EditUser.as_view(), name='edit_user'),
	url(r'^designation_list/$', DesignationList.as_view(), name="designation_list"),
	url(r'^add_designation/$', AddDesignation.as_view(), name="add_designation"),	
)