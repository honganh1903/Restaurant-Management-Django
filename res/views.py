from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .models import *



@staff_member_required
def dashboard(request): 
    return render(request, 'admin/dashboard.html')

# DISH


def add_dish(request):
    if request.method == 'POST':
        name = request.POST['name']
        status = request.POST['status']
        price = request.POST['price']
        menu_value = request.POST.get('menu')
        menu_instance = Menu.objects.get(type=menu_value)
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        if (name == "")  or (status is None) or (menu_instance is None) or (price == "") :
            dishs = Dish.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'res : dish_list', {'dishs': dishs, 'error_msg': error_msg})

        dish = Dish.objects.create(name=name,  status=status, menu=menu_instance,
                                   price=price, image=filename)
        dish.save()
        dishs = Dish.objects.filter()
    return redirect(reverse('res:dish_list'))

def dish_list(request): 
    dishes = Dish.objects.all()
    return render(request, 'admin/dish.html', {'dishes': dishes})

@login_required
@staff_member_required
def edit_food(request, dishID):
    dish = Dish.objects.filter(id=dishID)[0]
    if request.method == "POST":
        if request.POST['price'] != "":
            dish.price = request.POST['price']

        if request.POST['discount'] != "":
            dish.discount = request.POST['discount']

        status = request.POST.get('disabled')
        if status == 'on':
            dish.status = "Disabled"
        else:
            dish.status = "Enabled"

        dish.save()
    return redirect('hotel:dishs_admin')


# CUSTOMER

def customer_list(request): 
    customers = Customer.objects.all()
    return render(request, 'admin/customer.html', {'customers': customers})

# EMPLOEE

def employee_list(request): 
    employees = Employee.objects.all()
    return render(request, 'admin/employee.html', {'employees': employees})

# ORDER

def order_list(request): 
    orders = Order.objects.all()
    return render(request, 'admin/order.html', {'orders': orders})
