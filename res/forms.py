from django import forms
from .models import Dish, Menu

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