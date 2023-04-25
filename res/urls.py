from django.urls import re_path
from .views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from res import views



urlpatterns = [
    re_path(r'^$',Login, name='login'),
    re_path(r'^home$',home, name='home'),
    re_path(r'^accounts/login/$',Login,name='login'),
    re_path(r'^accounts/logout/$', auth_views.LogoutView.as_view(),
            name='logout', kwargs={'next_page': '/'}),
    re_path(r'^dashboard$',dashboard, name='dashboard'),
    re_path(r'^dashboard/dish_list/$',dish_list, name='dish_list'),
    re_path(r'^dashboard/customer_list/$',customer_list, name='customer_list'),
    re_path(r'^dashboard/employee_list$',employee_list, name='employee_list'),
    re_path(r'^dashboard/order_list$',order_list, name='order_list'),
]
