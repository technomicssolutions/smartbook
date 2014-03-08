from django.conf.urls import patterns, include, url

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', Logout.as_view(), name='logout'),
	url(r'^vendor-list/$', VendorList.as_view(),name='vendor'),
	url(r'^add-vendor/$', VendorAdd.as_view(),name='vendoradd'),
	url(r'^staff-list/$', StaffList.as_view(),name='staff'),
	url(r'^add-staff/$', StaffAdd.as_view(),name='staffadd'),
	url(r'^customer-list/$', CustomerList.as_view(),name='customer'),
	url(r'^add-customer/$', CustomerAdd.as_view(),name='customeradd'),
)