from django.contrib import admin
from django.conf.urls import url
from .views import (
	UserCreateAPIView, 
	UserLoginAPIView,
	UserChangePasswordAPIView,
	)

urlpatterns = [
    url(r'^signup/?', UserCreateAPIView.as_view(), name='signup'),
    url(r'^login/?', UserLoginAPIView.as_view(), name='login'),
    url(r'^change_password/?', UserChangePasswordAPIView.as_view(), name='change_password'),
]