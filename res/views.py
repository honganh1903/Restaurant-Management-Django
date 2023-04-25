from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

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
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        if (address == "") or (number_phone == ""):
            customers = Customer.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'res: customer_list', {'customers': customers, 'error_msg': error_msg})
        
        # Use the newly created user instance to create an customer
        customer = Customer.objects.create(customer=user, address=address, number_phone=number_phone)
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
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)
        if (address == "") or (number_phone == ""):
            employees = Employee.objects.filter()
            error_msg = "Please enter valid details"
            return render(request, 'res: employee_list', {'employees': employees, 'error_msg': error_msg})
        
        # Use the newly created user instance to create an employee
        employee = Employee.objects.create(employee=user, address=address, number_phone=number_phone)
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
        return render(request, 'res: edit_employee', {'employee': employee})

@login_required
@staff_member_required
def delete_employee(request, employeeID):
    employee = Employee.objects.get(id=employeeID)
    employee.employee.delete()
    employee.delete()
    return redirect(reverse('res:employee_list'))

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
