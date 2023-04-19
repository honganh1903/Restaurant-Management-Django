from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Student
from .forms import FoodForm
from .models import Dish


def home(request):
    students = Student.objects.all()
    return render(request, 'res/home.html', {"students": students})


@staff_member_required
def add_dish(request):
    if request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            # Điều hướng sau khi thêm món ăn thành công
            return redirect(reverse('res:food_list'))
        else:
             print(form.errors)
    else:
        form = FoodForm()
    return redirect(reverse('res:food_list'))


def food_list(request):
    foods = Dish.objects.all()
    return render(request, 'admin/food.html', {'foods': foods})
