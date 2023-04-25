from .models import *
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
<< << << < HEAD
# from .forms import DishForm
== == == =

>>>>>> > b4a3c8112d106006421a7c71a87e8d22ec9674bc


@login_required
@staff_member_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')

# DISH


<< << << < HEAD
#             return redirect('/admin/dish_list') # Điều hướng sau khi thêm món ăn thành công
#     else:
#         form = DishForm()
#     return render(request, 'admin/add_dish.html', {'form': form})
def dish_list(request):


== == == =


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
        if (name == "") or (status is None) or (menu_instance is None) or (price == ""):
            dishs = Dish.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'res : dish_list', {'dishs': dishs, 'error_msg': error_msg})

        dish = Dish.objects.create(name=name,  status=status, menu=menu_instance,
                                   price=price, image=filename)
        dish.save()
        dishs = Dish.objects.filter()
    return redirect(reverse('res:dish_list'))


def dish_list(request):


>>>>>> > b4a3c8112d106006421a7c71a87e8d22ec9674bc
dishes = Dish.objects.all()
return render(request, 'admin/dish.html', {'dishes': dishes})


@login_required
@staff_member_required
def edit_dish(request, dishID):
    dish = Dish.objects.get(id=dishID)

    if request.method == "POST":
        print('Update')
        dish.name = request.POST.get('name', dish.name)
        dish.menu = Menu.objects.get(
            type=request.POST.get('menu', dish.menu.type))

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


def cart_list(request):
    carts = Cart.objects.all()
    list_cart = []
    for elm in carts:
        cart = []
        total = 0
        orders = Order.objects.filter(cart_id=elm.id)
        for order in orders:
            dish = Dish.objects.get(id=order.food_id)
            cart.append(dish)
            total = total + dish.price * order.amount
            cart.append(order.amount)
        cart.append(total)
        list_cart.append(cart)
    for elm in list_cart:
        print(elm)
    return render(request, 'admin/cart.html', {'list_cart': list_cart})
