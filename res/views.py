from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

# from .forms import DishForm
from .models import *



@staff_member_required
def dashboard(request): 
    return render(request, 'admin/dashboard.html')

# DISH


# def add_dish(request):
#     if request.method == 'POST':
#         form = DishForm(request.POST)
#         if form.is_valid():
#             form.save()

#             return redirect('/admin/dish_list') # Điều hướng sau khi thêm món ăn thành công
#     else:
#         form = DishForm()
#     return render(request, 'admin/add_dish.html', {'form': form})
def dish_list(request): 
    dishes = Dish.objects.all()
    return render(request, 'admin/dish.html', {'dishes': dishes})

# CUSTOMER

def customer_list(request): 
    customers = Customer.objects.all()
    for customer in customers:
        user = User.objects.get(id=customer.customer_id)
        customer.username = user.username
        customer.name = user.first_name + ' ' + user.last_name
    return render(request, 'admin/customer.html', {'customers': customers})

# EMPLOEE

def employee_list(request): 
    employees = Employee.objects.all()
    for employee in employees:
        user = User.objects.get(id=employee.employee_id)
        employee.username = user.username
        employee.name = user.first_name + ' ' + user.last_name

    return render(request, 'admin/employee.html', {'employees': employees})
# ORDER

def order_list(request): 
    orders = Order.objects.all()
    return render(request, 'admin/order.html', {'orders': orders})
