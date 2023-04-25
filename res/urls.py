from django.urls import re_path
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path(r'^dashboard$',dashboard, name='dashboard'),
    re_path(r'^dashboard/dish_list/$',dish_list, name='dish_list'),
    re_path(r'^dashboard/add_dish/$',add_dish, name='add_dish'),
    re_path(r'^dashboard/edit_dish/(?P<dishID>\d+)/$',edit_dish, name='edit_dish'),
    re_path(r'^dashboard/delete_dish/(?P<dishID>\d+)/$',delete_dish, name='delete_dish'),
    re_path(r'^dashboard/delete_dish_in_cart/(?P<dishID>\d+)/$',delete_dish_in_cart, name='delete_dish_in_cart'),
    re_path(r'^dashboard/customer_list/$',customer_list, name='customer_list'),
    re_path(r'^dashboard/employee_list$',employee_list, name='employee_list'),
    re_path(r'^dashboard/cart_list$',cart_list, name='cart_list'),
    re_path(r'^dashboard/cart_detail/(?P<cartID>\d+)/$',cart_detail, name='cart_detail'),
    re_path(r'^show_html$', show_html, name='show_html'),
]
