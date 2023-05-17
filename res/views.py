from .models import *
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import *
from datetime import datetime

from .forms import *

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Q

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
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            
            user_check = authenticate(request, username = user.username)
            if user_check is None:
                user.save()
                address = form.cleaned_data['address']
                number_phone = form.cleaned_data['number_phone']
                customer = Customer.objects.create(
                    customer=user, address=address, number_phone=number_phone)
                customer.save()
            else:
                messages.error(request, 'Email is available')
                return redirect('http://localhost:8000/accounts/signup')
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
                return redirect('res:home')
        else:
            messages.error(request, 'Please check your username and password again !')
            return redirect('/accounts/login')
    return render(request, 'registration/login.html')

# DISH

@login_required
@staff_member_required
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
            messages.error(request, "Please enter valid details")
            return render(request, 'res : dish_list', {'dishs': dishs})
        
        if Dish.objects.filter(name=name).exists():
            dishs = Dish.objects.filter()
            messages.error(request, "Dish with this name already exists.")
            return redirect(reverse('res:dish_list', {'dishs': dishs}))

        if Dish.objects.filter(image=filename).exists():
            dishs = Dish.objects.filter()
            messages.error(request, "Dish with this image already exists.")
            return redirect(reverse('res:dish_list', {'dishs': dishs}))
        dish = Dish.objects.create(name=name,  status=status, menu=menu_instance,
                                   price=price, image=filename)
        
        messages.success(request, f"Created customer {dish} successfully")
        
        dish.save()
        dishs = Dish.objects.filter()
    return redirect(reverse('res:dish_list', {'dishs': dishs}))


def dish_list(request):
    dishes = Dish.objects.all()
    return render(request, 'admin/dish.html', {'dishes': dishes})


@login_required
@staff_member_required
def edit_dish(request, dishID):
    dish = Dish.objects.get(id=dishID)

    if request.method == "POST":
        nameEdit = request.POST.get('name', dish.name)
        if Dish.objects.filter(name=nameEdit).exists():
            dishs = Dish.objects.filter()
            messages.error(request, "Dish with this name already exists.")
            return redirect(reverse('res:dish_list', {'dishs': dishs}))

        status = request.POST.get('status')
        if status:
            dish.status = status

        image = request.FILES.get('image-edit')
        if image:
            dish.image = image

        dish.price = request.POST.get('price', dish.price)

        dish.menu = Menu.objects.get(
        type=request.POST.get('menu', dish.menu.type))

        dish.name = nameEdit

        messages.success(request, f"Created customer {dish} successfully")

        dish.save()

    return redirect(reverse('res:dish_list'))


@login_required
@staff_member_required
def delete_dish(request, dishID):
    item = Dish.objects.get(id=dishID)
    if (request.method != 'POST') or item is None:
        messages.error(request, f"Not found dish has ID: {dishID}")
    else:
        item.delete()
        messages.success(request, f"Delete dish has ID: {dishID}")
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

        # Check if username is unique
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username has already been taken!')
            return redirect(reverse('res:customer_list'))

        # Check if the password and confirmation password match
        if password != confirm_password:
            messages.error(request, 'Password does not match!')
            return redirect(reverse('res:customer_list'))
        
        # Create a new user instance
        user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password, email=email)

        if (address == "") or (number_phone == ""):
            messages.error(request, "Please enter valid details")
            return redirect(reverse('res:customer_list'))

        # Use the newly created user instance to create an customer
        customer = Customer.objects.create(
            customer=user, address=address, number_phone=number_phone)
        customer.save()

        user.is_staff = False
        user.save()
        messages.success(request, f"Created customer {customer} successfully")

    return redirect(reverse('res:customer_list'))


@login_required
@staff_member_required
def edit_customer(request, customerID):
    customer = Customer.objects.get(id=customerID)
    if request.method == 'POST':
        address = request.POST['address']
        number_phone = request.POST['number_phone']

        if (address == "") or (number_phone == ""):
            messages.error(request, "Please enter valid details")
            return render(request, 'res: edit_customer', {'customer': customer})

        customer.address = address
        customer.number_phone = number_phone
        customer.save()
        messages.success(request, f"Updated customer {customer} successfully")
        return redirect(reverse('res:customer_list'))
    else:
        return render(request, 'res:edit_customer', {'customer': customer})


@login_required
@staff_member_required
def delete_customer(request, customerID):
    customer = Customer.objects.get(id=customerID)
    if request.method != 'POST' and customer is None:
        messages.error(request, "Customer is not found !!!")

    else:
        customer.customer.delete()
        customer.delete()
        messages.success(request, "Delete customer successfully !!!")
        return redirect(reverse('res:customer_list'))
    return render(request, 'res:delete_customer', {'customer': customer})


# EMPLOEE
@login_required
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

        # Check if username is unique
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username has already been taken!')
            return redirect(reverse('res:employee_list'))

        # Check if the password and confirmation password match
        if password != confirm_password:
            messages.error(request, 'Password does not match!')
            return redirect(reverse('res:employee_list'))
        
        # Create a new user instance
        user = User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name, password=password, email=email)

        if (address == "") or (number_phone == ""):
            messages.error(request, "Please enter valid details")
            return redirect(reverse('res:employee_list'))

        # Use the newly created user instance to create an employee
        employee = Employee.objects.create(
            employee=user, address=address, number_phone=number_phone)
        employee.save()

        user.is_staff = True
        user.save()
        messages.success(request, f"Created employee {employee} successfully")

    return redirect(reverse('res:employee_list'))


@login_required
@staff_member_required
def edit_employee(request, employeeID):
    employee = Employee.objects.get(id=employeeID)
    if request.method == 'POST':
        address = request.POST['address']
        number_phone = request.POST['number_phone']

        if (address == "") or (number_phone == ""):
            messages.error(request, "Please enter valid details")
            return render(request, 'res: edit_employee', {'employee': employee})

        employee.address = address
        employee.number_phone = number_phone
        employee.save()
        messages.success(request, f"Updated employee {employee} successfully")
        return redirect(reverse('res:employee_list'))
    else:
        return render(request, 'res:edit_employee', {'employee': employee})


@login_required
@staff_member_required
def delete_employee(request, employeeID):
    if request.method == 'POST':
        employee = Employee.objects.get(id=employeeID)
        employee.employee.delete()
        employee.delete()
        messages.success(request, "Delete employee successfully !!!")
        return redirect(reverse('res:employee_list'))
    else:
        return render(request, 'res:delete_employee', {'employee': employee})
# CART

@login_required
@staff_member_required
def cart_detail_admin(request, cartID, status):
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
    return render(request, 'admin/cart_detail.html', {'detail': detail,'cartID' :cartID,'status':status})

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
    return render(request, 'res/home.html', {'menu': menu})


def menu(request):
    menu = Menu.objects.all()
    return render(request, 'res/menu.html', {'menu': menu})


# @login_required
def menu_details(request, id):
    menu = Menu.objects.get(id=id)
    dishes = Dish.objects.filter(menu=menu)
    return render(request, 'res/dish_list.html', {'dishes': dishes, 'menu': menu})


@login_required
def dish_details(request, id):
    dish = Dish.objects.get(id=id)
    return render(request, 'res/dish_details.html', {'dish': dish})

@login_required
def list_invoice(request):
    customer = Customer.objects.get(customer_id = request.user.id)
    # cart = Cart.objects.filter(customer_id=customer, status = 'Completed' or status = 'Processing')
    items = Cart.objects.filter(Q(customer_id=customer) & (Q(status='Completed') | Q(status='Processing')))
    # items = Order.objects.filter(cart=cart)
    return render(request, 'res/list_invoice.html', {'items': items})

@login_required
def invoice_details(request, cartID):
    cart = Cart.objects.get(id = cartID)
    items = Order.objects.filter(cart=cart)
    total = 0
    for item in items:
        total += item.dish.price*item.amount
    cart.total = total
    cart.save()
    return render(request, 'res/invoice_details.html', {'items': items, 'total': total})
@login_required
def list_invoice(request):
    customer = Customer.objects.get(customer_id = request.user.id)
    # cart = Cart.objects.filter(customer_id=customer, status = 'Completed' or status = 'Processing')
    items = Cart.objects.filter(Q(customer_id=customer) & (Q(status='Completed') | Q(status='Processing')))
    # items = Order.objects.filter(cart=cart)
    return render(request, 'res/list_invoice.html', {'items': items})

@login_required
def invoice_details(request, cartID):
    cart = Cart.objects.get(id = cartID)
    items = Order.objects.filter(cart=cart)
    total = 0
    for item in items:
        total += item.dish.price*item.amount
    cart.total = total
    cart.save()
    return render(request, 'res/invoice_details.html', {'items': items, 'total': total})

@login_required
def addTocart(request, dishID, userID):
    dish = Dish.objects.get(id=dishID)
    customer = Customer.objects.get(customer_id=userID)
    try:
        cart = Cart.objects.get(customer_id=customer, status = 'Pending')
    except Cart.DoesNotExist:
        cart = Cart.objects.create(customer_id=customer.id, employee_id = 1, date = datetime.now(), status = 'Pending', total = 0)
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
    customer = Customer.objects.get(customer_id = request.user.id)
    cart = Cart.objects.get(customer_id=customer, status = 'Pending')
    items = Order.objects.filter(cart=cart)
    total = 0
    for item in items:
        total += item.dish.price*item.amount
    cart.total = total
    cart.save()
    return render(request, 'res/cart.html', {'items': items, 'total': total})

@login_required
def placeOrder(request):
    customer = Customer.objects.get(customer_id = request.user.id)
    cart = Cart.objects.get(customer_id=customer, status = 'Pending')
    cart.status = 'Processing'
    cart.save()
    # return redirect('hotel:cart')
    return render(request, 'res/order_sucess.html')

@login_required
def profile(request):
    user = User.objects.get(id = request.user.id)
    customer = Customer.objects.get(customer = user)
    return render(request, 'res/profile.html', {'customer' : customer})
@login_required
def edit_profile(request, ID):
    customer = Customer.objects.get(id = ID)
    if request.method == "POST":
        customer.customer.first_name = request.POST['firstname']
        customer.customer.last_name = request.POST['lastname']
        customer.customer.email = request.POST['email']
        customer.address = request.POST['address']
        customer.number_phone = request.POST['phonenumber']
        customer.customer.username = request.POST['username']
        customer.save()
    return render(request, 'res/profile.html', {'customer' : customer})

def change_password(request, ID):
    customer = Customer.objects.get(id = ID)
    username = customer.customer.username
    if request.method == 'POST':
        curentpassword = request.POST.get('curentpassword')
        newpassword = request.POST.get('newpassword')
        user = authenticate(request, username=username, password=curentpassword)
        if user is not None:
            user.set_password(newpassword)
            user.save()
            messages.success(request, f'Change Password Successful! Please login again.')
            return redirect('/accounts/login')
        else:
            messages.error(request, 'Update password failed! Please check your username and password again !')
            return render(request, 'res/profile.html', {'customer' : customer})
    return render(request, 'res/profile.html', {'customer' : customer})


def delete_dish_in_cart(request, cartID,dishID):
    cart = Cart.objects.get(id = cartID)
    oder = Order.objects.get(dish_id = dishID)
    if request.method == 'POST':
        print('Delete')
        oder.delete()
    return redirect(reverse('res:cart_detail'))
