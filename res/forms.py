from django import forms
from .models import Student
from .models import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'address', 'roll', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'roll': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'status', 'price', 'image']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        # fields = ['name','username', 'email', 'address','number_phone']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'address': forms.TextInput(attrs={'class': 'form-control'}),
        #     'address': forms.TextInput(attrs={'class': 'form-control'}),
        #     'number_phone': forms.TextInput(attrs={'class': 'form-control'}),
        # }
        fields = ['address','number_phone']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'number_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }