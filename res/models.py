from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    roll = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    number_phone = models.TextField(max_length = 10)
    username = User.username
    password = User.password

    def __str__(self):
        return self.customer.first_name + " " + self.customer.last_name


class Employee(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    number_phone = models.TextField(max_length = 10)
    username = User.username
    password = User.password

    def __str__(self):
        return self.employee.first_name + " " + self.employee.last_name
    
class Dish(models.Model):
    disabled = 'Disabled'
    enabled = 'Enabled'

    STATUS = (
        (disabled, disabled),
        (enabled, enabled),
    )

    name = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=STATUS)
    price = models.FloatField()
    image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    pending = 'Pending'
    completed = 'Completed'
    STATUS = (
        (pending, pending),
        (completed, completed),
    )
    pickup = 'PickUp'
    delivery = 'Delivery'

    TYPE = (
        (pickup, pickup),
        (delivery, delivery),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    is_delivery = models.BooleanField(default="False")
    is_paid = models.BooleanField(default="False")
    total = models.IntegerField(default=0)
    date = models.DateTimeField()
    status = models.CharField(max_length=100, choices=STATUS)
    type = models.CharField(max_length=100, choices=TYPE)

    def __str__(self):
        return self.customer.__str__() + " " + self.date.__str__()


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    food = models.ForeignKey(Dish, on_delete=models.CASCADE)
    amount = models.IntegerField()
    details = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.cart.__str__()
