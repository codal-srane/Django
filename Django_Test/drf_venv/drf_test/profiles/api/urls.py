from django.contrib import admin
from django.conf.urls import url
from .views import UserCreateAPIView, UserLoginAPIView

urlpatterns = [
    url(r'^signup/?', UserCreateAPIView.as_view(), name='signup'),
    url(r'^login/?', UserLoginAPIView.as_view(), name='login')
]