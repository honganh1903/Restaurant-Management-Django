from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import *

# from .forms import DishForm
from .forms import *

from django.contrib.auth.decorators import login_required


@login_required
@staff_member_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')

#home
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.email = form.cleaned_data['email']
            user.username = user.email.split('@')[0]
            user.set_password(form.cleaned_data['password'])
            user.save()
            address = form.cleaned_data['address']
            number_phone = form.cleaned_data['number_phone']
            customer = Customer.objects.create(
                customer=user, address=address, number_phone=number_phone)
            customer.save()
            return redirect('http://localhost:8000/accounts/login')

    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)       
        if user is not None:
            check = user.is_staff
            if check :
                form = login(request,user)
                return redirect('dashboard')
            else:   
                form = login(request,user)            
                return redirect('home')
        else:
            messages.error(request, 'Please check your username and password again !')
            return redirect('/accounts/login')
    return render(request, 'registration/login.html')

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


@login_required
@staff_member_required
def add_customer(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address = request.POST['address']
        number_phone = request.POST['number_phone']

        # Check if the password and confirmation password match
        if password != confirm_password:
            customers = Customer.objects.filter()
            error_msg = "Passwords do not match"
            return render(request, 'res: customer_list', {'customers': customers, 'error_msg': error_msg})

        # Create a new user instance
        user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        if (address == "") or (number_phone == ""):
            customers = Customer.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'res: customer_list', {'customers': customers, 'error_msg': error_msg})

        # Use the newly created user instance to create an customer
        customer = Customer.objects.create(
            customer=user, address=address, number_phone=number_phone)
        customer.save()

        user.is_staff = True
        user.save()

        customers = Customer.objects.filter()
    return redirect(reverse('res:customer_list'))


@login_required
@staff_member_required
def edit_customer(request, customerID):
    customer = Customer.objects.get(id=customerID)
    if request.method == 'POST':
        address = request.POST['address']
        number_phone = request.POST['number_phone']

        if (address == "") or (number_phone == ""):
            error_msg = "Please enter valid details"
            return render(request, 'res: edit_customer', {'customer': customer, 'error_msg': error_msg})

        customer.address = address
        customer.number_phone = number_phone
        customer.save()

        return redirect(reverse('res:customer_list'))
    else:
        return render(request, 'res: edit_customer', {'customer': customer})


@login_required
@staff_member_required
def delete_customer(request, customerID):
    customer = Customer.objects.get(id=customerID)
    customer.customer.delete()
    customer.delete()
    return redirect(reverse('res:customer_list'))


# EMPLOEE
@login_required
@staff_member_required
def employee_list(request):
    employees = Employee.objects.all()

    for employee in employees:
        user = User.objects.get(id=employee.employee_id)
        employee.username = user.username
        employee.name = user.first_name + ' ' + user.last_name

    return render(request, 'admin/employee.html', {'employees': employees})


@login_required
@staff_member_required
def add_employee(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        address = request.POST['address']
        number_phone = request.POST['number_phone']

        # Check if the password and confirmation password match
        if password != confirm_password:
            employees = Employee.objects.filter()
            error_msg = "Passwords do not match"
            return render(request, 'res: employee_list', {'employees': employees, 'error_msg': error_msg})

        # Create a new user instance
        user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        if (address == "") or (number_phone == ""):
            employees = Employee.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'res: employee_list', {'employees': employees, 'error_msg': error_msg})

        # Use the newly created user instance to create an employee
        employee = Employee.objects.create(
            employee=user, address=address, number_phone=number_phone)
        employee.save()

        user.is_staff = True
        user.save()

        employees = Employee.objects.filter()
    return redirect(reverse('res:employee_list'))


@login_required
@staff_member_required
def edit_employee(request, employeeID):
    employee = Employee.objects.get(id=employeeID)
    if request.method == 'POST':
        address = request.POST['address']
        number_phone = request.POST['number_phone']

        if (address == "") or (number_phone == ""):
            error_msg = "Please enter valid details"
            return render(request, 'res: edit_employee', {'employee': employee, 'error_msg': error_msg})

        employee.address = address
        employee.number_phone = number_phone
        employee.save()

        return redirect(reverse('res:employee_list'))
    else:
        return render(request, 'res:edit_employee', {'employee': employee})


@login_required
@staff_member_required
def delete_employee(request, employeeID):
    employee = Employee.objects.get(id=employeeID)
    employee.employee.delete()
    employee.delete()
    return redirect(reverse('res:employee_list'))

# CART

@login_required
@staff_member_required
def cart_detail(request, cartID):
    detail = []
    total = 0
    orders = Order.objects.filter(cart_id=cartID)
    for order in orders:
        order_detail = {}
        dish = Dish.objects.get(id = order.dish_id)
        total = total + dish.price * order.amount
        order_detail[order.id] = [dish,order.details,order.amount]
        detail.append(order_detail)
    total1 = {"total": total}
    detail.append(total1)
    return render(request, 'admin/cart_detail.html', {'detail': detail,'cartID' :cartID})

@login_required
@staff_member_required
def edit_cart(request, cartID):
    cart = Cart.objects.get(id=cartID)
    if request.method == 'POST':
        cart.status = "Completed"
        cart.save()
        if request.POST.get('confirm') == 'true':
            cart.status = "Completed"
            cart.save()
        elif request.POST.get('change') == 'true':
            cart.status = "Completed"
            if cart.type == "PickUp":
                cart.type = "Delivery"
            else:
                cart.type = "PickUp"    
            cart.save()
    return redirect(reverse('res:cart_list'))

@login_required
@staff_member_required
def cart_list(request):
    carts = Cart.objects.all()
    return render(request, 'admin/cart.html', {'carts': carts})

@login_required
@staff_member_required
def delete_item_in_cart(request, ID,cartID):
    item = Order.objects.get(id=ID)
    if request.method == "POST":
        item.delete()
        return redirect(reverse('res:cart_detail', args=[cartID]))

def home(request):
    last_item = Menu.objects.last()
    menu = Menu.objects.exclude(id=last_item.id)
    return render(request, 'admin/menu.html', {'menu': menu})


def menu(request):
    menu = Menu.objects.all()
    return render(request, 'res/menu.html', {'menu': menu})


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
    if request.method == "POST":
        item.delete()
        return redirect(reverse('res:cart_detail'))
    else:
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


def delete_dish_in_cart(request, cartID,dishID):
    cart = Cart.objects.get(id = cartID)
    oder = Order.objects.get(dish_id = dishID)
    if request.method == 'POST':
        print('Delete')
        oder.delete()
    return redirect(reverse('res:cart_detail'))
