from django.urls import re_path
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path(r'^$', home, name='home'),
    re_path(r'^dashboard$', dashboard, name='dashboard'),
    re_path(r'^menu/$', menu, name='menu'),
    re_path(r'^menu/menu_details/(?P<id>\d+)/$',
            menu_details, name='menu_details'),
    re_path(r'^menu/dish_list/dish_details/(?P<id>\d+)/$',
            dish_details, name='dish_details'),
    re_path(r'^dashboard/dish_list/$', dish_list, name='dish_list'),
    re_path(r'^dashboard/customer_list/$',
            customer_list, name='customer_list'),
    re_path(r'^dashboard/employee_list$', employee_list, name='employee_list'),
    re_path(r'^dashboard/order_list$', order_list, name='order_list'),
    re_path(r'^order/$', order, name='order'),
    re_path(r'^addTocart/(?P<dishID>\d+)/(?P<userID>\d+)/$',
            addTocart, name='addTocart'),
    re_path(r'^delete_item/(?P<ID>\d+)/$', delete_item, name='delete_item'),
    re_path(r'^edit_item/(?P<ID>\d+)/$', edit_item, name='edit_item'),
]
