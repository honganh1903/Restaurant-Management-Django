from django.contrib import admin
from .models import Customer, Employee, Order, Dish, Menu, Cart, Student

# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Dish)
admin.site.register(Employee)
admin.site.register(Menu)
admin.site.register(Cart)
admin.site.register(Student)
