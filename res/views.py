from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
# from .forms import DishForm
from .models import *


@login_required
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
    return render(request, 'admin/customer.html', {'customers': customers})

# EMPLOEE


def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'admin/employee.html', {'employees': employees})

# ORDER


def order_list(request):
    orders = Order.objects.all()
    return render(request, 'admin/order.html', {'orders': orders})


def home(request):
    last_item = Menu.objects.last()
    menu = Menu.objects.exclude(id=last_item.id)
    return render(request, 'res/home.html', {'menu': menu})


def menu(request):
    # cuisine = request.GET.get('cuisine')
    # # print(cuisine)
    # if cuisine is not None:
    #     if ((cuisine == "Gujarati") or (cuisine == "Punjabi")):
    #         foods = Dish.objects.filter(status="Enabled", course=cuisine)
    #     elif (cuisine == "south"):
    #         foods = Dish.objects.filter(
    #             status="Enabled", course="South Indian")
    #     elif (cuisine == "fast"):
    #         foods = Dish.objects.filter(course="Fast")
    # else:
    menu = Menu.objects.all()
    return render(request, 'res/menu.html', {'menu': menu})
    # , 'cuisine': cuisine


@login_required
def menu_details(request, id):
    menu = Menu.objects.get(id=id)
    dishes = Dish.objects.filter(menu=menu)
    return render(request, 'res/dish_list.html', {'dishes': dishes, 'menu': menu})


@login_required
def dish_details(request, id):
    dish = Dish.objects.get(id=id)
    return render(request, 'res/dish_details.html', {'dish': dish})


@login_required
def addTocart(request, dishID, userID):
    dish = Dish.objects.get(id=dishID)
    cart = Cart.objects.get(id=1)
    quantity = request.POST.get('quantity', 1)
    requirement = request.POST.get('requirement', "")
    order = Order.objects.create(
        cart=cart, dish=dish, amount=quantity, details=requirement)
    order.save()
    return redirect('res:order')


@login_required
def delete_item(request, ID):
    item = Order.objects.get(id=ID)
    item.delete()
    return redirect('res:order')


@login_required
def edit_item(request, ID):
    order = Order.objects.filter(id=ID)[0]
    if request.method == "POST":
        order.amount = request.POST['amount']
        order.details = request.POST['details']
        order.save()
    return redirect('res:order')


@login_required
def order(request):
    # user = User.objects.get(id=request.user.id)
    items = Order.objects.filter(cart_id=1)
    total = 0
    for item in items:
        total += item.dish.price*item.amount
    return render(request, 'res/cart.html', {'items': items, 'total': total})
