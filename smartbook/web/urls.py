from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from django.conf import settings

from web.views import *

urlpatterns = patterns('',
	url(r'^$', Home.as_view(), name='home'),
	url(r'login/$', Login.as_view(), name='login'),
	url(r'logout/$', login_required(Logout.as_view()), name='logout'),
	url(r'^register/(?P<user_type>\w+)/$', login_required(RegisterUser.as_view()), name='register_user'),
	url(r'^register/salesman/(?P<user_type>\w+)/$', login_required(RegisterSalesman.as_view()), name='register_salesman'),
	url(r'^(?P<user_type>\w+)/list/$', login_required(UserList.as_view()), name='users'),
	url(r'^(?P<user_type>\w+)/(?P<user_id>\d+)/edit/$', login_required(EditUser.as_view()), name='edit_user'),
	url(r'^(?P<user_type>\w+)/(?P<user_id>\d+)/delete/$', login_required(DeleteUser.as_view()), name='delete_user'),
	url(r'^company_list/$', login_required(TransportationCompanyList.as_view()), name="company_list"),
	url(r'^add_company/$', login_required(AddTransportationCompany.as_view()), name="add_company"),
	url(r'^reset_password/(?P<user_id>\d+)/$', login_required(ResetPassword.as_view()), name="reset_password"),
	url(r'^backup/$', login_required(BackupView.as_view()), name="backup"),
	url(r'^clear_backup/$', login_required(ClearBackup.as_view()), name="clear_backup"),
	url(r'^backups/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	url(r'^create_customer/$', login_required(CreateCustomer.as_view()), name='create_customer'),
)