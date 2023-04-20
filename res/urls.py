from django.urls import re_path
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path(r'^dashboard$',dashboard, name='dashboard'),
    re_path(r'^dashboard/dish_list/$',dish_list, name='dish_list'),
    re_path(r'^dashboard/add_dish/$',add_dish, name='add_dish'),
    re_path(r'^dashboard/customer_list/$',customer_list, name='customer_list'),
    re_path(r'^dashboard/employee_list$',employee_list, name='employee_list'),
    re_path(r'^dashboard/cart_list$',cart_list, name='cart_list'),
]
