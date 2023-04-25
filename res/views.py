from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import *

# from .forms import DishForm
from .models import *
from .forms import *



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
        check = user.is_staff
        if user is not None:
            if check :
                form = login(request,user)
                return redirect('dashboard')
            else:   
                form = login(request,user)            
                return redirect('home')
        else:
            return render()
    return render(request, 'registration/login.html')
def home(request):

    return render(request, 'res/home.html')

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
