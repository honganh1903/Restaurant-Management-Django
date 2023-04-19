from django.contrib import admin
from .models import Customer, Employee, Order, Dish,Cart,Menu

admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Order)
admin.site.register(Dish)
admin.site.register(Cart)
admin.site.register(Menu)