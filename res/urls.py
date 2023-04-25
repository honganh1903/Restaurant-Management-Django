from django.urls import re_path
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path(r'^dashboard$',dashboard, name='dashboard'),

    # Dish routes
    re_path(r'^dashboard/dish_list/$',dish_list, name='dish_list'),
    re_path(r'^dashboard/add_dish/$',add_dish, name='add_dish'),
    re_path(r'^dashboard/edit_dish/(?P<dishID>\d+)/$',edit_dish, name='edit_dish'),
    re_path(r'^dashboard/delete_dish/(?P<dishID>\d+)/$',delete_dish, name='delete_dish'),

    # Customer routes
    re_path(r'^dashboard/customer_list/$',customer_list, name='customer_list'),
    re_path(r'^dashboard/add_customer$',add_customer, name='add_customer'),
    re_path(r'^dashboard/edit_customer/(?P<customerID>\d+)/$',edit_customer, name='edit_customer'),
    re_path(r'^dashboard/delete_customer/(?P<customerID>\d+)/$',delete_customer, name='delete_customer'),
    # Employee routes
    re_path(r'^dashboard/employee_list$',employee_list, name='employee_list'),
    re_path(r'^dashboard/add_employee$',add_employee, name='add_employee'),
    re_path(r'^dashboard/edit_employee/(?P<employeeID>\d+)/$',edit_employee, name='edit_employee'),
    re_path(r'^dashboard/delete_employee/(?P<employeeID>\d+)/$',delete_employee, name='delete_employee'),

    # Cart routes
    re_path(r'^dashboard/cart_list$',cart_list, name='cart_list'),
]
