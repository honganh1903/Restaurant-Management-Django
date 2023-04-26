from django.urls import re_path
from .views import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from res import views



urlpatterns = [
    re_path(r'login^$',Login, name='login'),
    re_path(r'^accounts/login/$',Login,name='login'),
    re_path(r'^accounts/logout/$', auth_views.LogoutView.as_view(),
            name='logout', kwargs={'next_page': '/'}),
    re_path(r'^$', home, name='home'),
    re_path(r'^menu/$', menu, name='menu'),
    re_path(r'^menu/menu_details/(?P<id>\d+)/$',
            menu_details, name='menu_details'),
    re_path(r'^menu/dish_list/dish_details/(?P<id>\d+)/$',
            dish_details, name='dish_details'),
    re_path(r'^order/$', order, name='order'),
    re_path(r'^addTocart/(?P<dishID>\d+)/(?P<userID>\d+)/$',
            addTocart, name='addTocart'),
    re_path(r'^delete_item/(?P<ID>\d+)/$', delete_item, name='delete_item'),
    re_path(r'^edit_item/(?P<ID>\d+)/$', edit_item, name='edit_item'),

    re_path(r'^dashboard$', dashboard, name='dashboard'),

    # Dish routes

    re_path(r'^dashboard/dish_list/$',dish_list, name='dish_list'),
    re_path(r'^dashboard/add_dish/$',add_dish, name='add_dish'),
    re_path(r'^dashboard/edit_dish/(?P<dishID>\d+)/$',edit_dish, name='edit_dish'),
    re_path(r'^dashboard/delete_dish/(?P<dishID>\d+)/$',delete_dish, name='delete_dish'),


    # Customer routes

    re_path(r'^dashboard/customer_list/$',
            customer_list, name='customer_list'),
    re_path(r'^dashboard/add_customer$', add_customer, name='add_customer'),
    re_path(r'^dashboard/edit_customer/(?P<customerID>\d+)/$',
            edit_customer, name='edit_customer'),
    re_path(r'^dashboard/delete_customer/(?P<customerID>\d+)/$',
            delete_customer, name='delete_customer'),
    # Employee routes
    re_path(r'^dashboard/employee_list$', employee_list, name='employee_list'),
    re_path(r'^dashboard/add_employee$', add_employee, name='add_employee'),
    re_path(r'^dashboard/edit_employee/(?P<employeeID>\d+)/$',
            edit_employee, name='edit_employee'),
    re_path(r'^dashboard/delete_employee/(?P<employeeID>\d+)/$',
            delete_employee, name='delete_employee'),

    # Cart routes

    re_path(r'^dashboard/cart_list$',cart_list, name='cart_list'),
    re_path(r'^dashboard/cart_detail/(?P<cartID>\d+)/$',cart_detail, name='cart_detail'),
    re_path(r'^dashboard/edit_cart/(?P<cartID>\d+)/$',edit_cart, name='edit_cart'),
    re_path(r'^delete_item_in_cart/(?P<ID>\d+)/(?P<cartID>\d+)/$', delete_item_in_cart, name='delete_item_in_cart'),
]
