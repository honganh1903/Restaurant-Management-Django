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
def edit_dish(request, dishID):
    dish = Dish.objects.get(id=dishID)

    if request.method == "POST":
        print('Update')
        dish.name = request.POST.get('name', dish.name)
        dish.menu = Menu.objects.get(type=request.POST.get('menu', dish.menu.type))

        status = request.POST.get('status')
        if status:
            dish.status = status

        dish.price = request.POST.get('price', dish.price)

        image = request.FILES.get('image-edit')
        if image:
            dish.image = image

        dish.save()
    return redirect(reverse('res:dish_list'))

@login_required
@staff_member_required
def delete_dish(request, dishID):
    item = Dish.objects.get(id=dishID)
    if request.method == 'POST':
        print('Delete')
        item.delete()
    return redirect(reverse('res:dish_list'))

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
