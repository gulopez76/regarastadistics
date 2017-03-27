from django.conf.urls import include, url, patterns
from . import views
from django.conf import settings

urlpatterns = (
	url(r'^$', views.index, name='index'),
	url(r'^login/$', views.login_user, name='login_user'),
	url(r'^logout/$', views.logout_user, name='logout_user'),
	url(r'^register$', views.register_user, name='register_user'),
	url(r'^usuthanks/(?P<username>[\w]+)/$', views.register_user_succesfull, name='register_user_succesfull'),
	url(r'^edit_email/$', views.edituser_email, name='edituser_email'),
	url(r'^edit_password/$', views.edituser_password, name='edituser_password'),
	url(r'^userprofile/(?P<pk>[0-9]+)/$', views.user_profile, name='user_profile'),
	url(r'^ots_deliver/$', views.ots_deliver_vw, name='ots_deliver_vw'),
	url(r'^carriers/$', views.carrier_vw, name='carrier_vw'),
	url(r'^carriers/(?P<pk>[0-9]+)/$', views.carrier_detail_vw, name='carrier_detail_vw'),
	url(r'^deliver/$', views.deliver_vw, name='deliver_vw'),
	url(r'^agentrights/$', views.agentrights_vw, name='agentrights_vw'),
	url(r'^agentrights/(?P<pk>[0-9]+)/$', views.agentrights_detail_vw, name='agentrights_detail_vw'),
)
