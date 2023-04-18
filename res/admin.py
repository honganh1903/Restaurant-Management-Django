from django.contrib import admin
from django.urls import path
from .views import *

class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_food/', self.admin_view(add_food), name='add_food'),
            path('food-list/', self.admin_view(food_list), name='food-list')
        ]
        return my_urls + urls

admin_site = MyAdminSite(name='myadmin')