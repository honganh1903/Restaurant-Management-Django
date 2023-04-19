from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

# from .forms import DishForm
from .models import *



@staff_member_required
def dashboard(request): 
    return render(request, 'admin/dashboard.html')

# DISH
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

# CART

def cart_list(request): 
    carts = Cart.objects.all()
    list_cart = []
    for elm in carts:
        cart = []
        total = 0
        orders = Order.objects.filter(cart_id=elm.id)
        for order in orders:
            dish = Dish.objects.get(id = order.food_id)
            cart.append(dish)
            total = total + dish.price * order.amount
            cart.append(order.amount)
        cart.append(total)
        list_cart.append(cart)
    for elm in list_cart:
        print(elm)
    return render(request, 'admin/cart.html', {'list_cart': list_cart})
