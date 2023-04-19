
from .models import Dish, Menu, Employee
from django import forms

class FoodForm(forms.ModelForm):
    menu = forms.ModelChoiceField(queryset=Menu.objects.filter(active=True))


    class Meta:
        model = Dish
        fields = ['name', 'status', 'price', 'image', 'menu']
        widgets = {
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'menu': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),

            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'})

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