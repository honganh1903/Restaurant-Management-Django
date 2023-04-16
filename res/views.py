from django.shortcuts import render, redirect
from .models import Student
from .forms import StudentForm

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
            student = Student(name=name, email=email, address=address, roll=roll, phone=phone)
            # Lưu đối tượng Student vào cơ sở dữ liệu
            student.save()
            print("Added") # In ra thông báo sau khi thêm dữ liệu thành công
            return redirect('/res/home') # Chuyển hướng đến trang chủ sau khi thêm dữ liệu
    else:
        form = StudentForm()
    return render(request, 'res/res_add.html', {'form': form})

def home(request):
    students = Student.objects.all()
    return render(request, 'res/home.html', {"students": students})