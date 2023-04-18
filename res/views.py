from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from .models import Student
from .forms import StudentForm
from .forms import FoodForm
from .models import Food


def res_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Lấy dữ liệu từ form
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            roll = form.cleaned_data['roll']
            phone = form.cleaned_data['phone']
            # Tạo một đối tượng Student mới với dữ liệu từ form
            student = Student(name=name, email=email,
                              address=address, roll=roll, phone=phone)
            # Lưu đối tượng Student vào cơ sở dữ liệu
            student.save()
            print("Added")  # In ra thông báo sau khi thêm dữ liệu thành công
            # Chuyển hướng đến trang chủ sau khi thêm dữ liệu
            return redirect('/res/home')
    else:
        form = StudentForm()
    return render(request, 'res/res_add.html', {'form': form})


def home(request):
    students = Student.objects.all()
    return render(request, 'res/home.html', {"students": students})


@staff_member_required
def add_food(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            # Điều hướng sau khi thêm món ăn thành công
            return redirect('/admin/food-list')
    else:
        form = FoodForm()
    return render(request, 'admin/add-food.html', {'form': form})


def food_list(request):
    foods = Food.objects.all()
    return render(request, 'admin/food.html', {'foods': foods})
