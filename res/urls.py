from django.urls import re_path
from .views import *
from django.contrib import admin

urlpatterns = [
    re_path(r'^$', home),
    re_path(r'^home/$', home),
    re_path(r'^add-student/$', res_add),
    re_path(r'^dashboard/food-list/$',
            food_list, name='food-list'),
]
