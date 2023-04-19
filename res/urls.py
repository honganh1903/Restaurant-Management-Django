from django.urls import re_path
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path(r'^$', home),
    re_path(r'^home/$', home),
    re_path(r'^add-student/$', res_add),
    re_path(r'^dashboard$',dashboard, name='dashboard'),
    re_path(r'^dashboard/dish_list/$',dish_list, name='dish_list'),
    re_path(r'^dashboard/customer_list/$',customer_list, name='customer_list'),
    re_path(r'^dashboard/employee_list$',employee_list, name='employee_list'),
    re_path(r'^dashboard/order_list$',order_list, name='order_list'),
]
