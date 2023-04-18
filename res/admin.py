from django.contrib import admin
from .models import Customer, Employee, Order, Food

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(Food)