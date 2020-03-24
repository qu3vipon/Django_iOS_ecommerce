from django.db import models

from members.models import User


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('quick', 'Quick'),
        ('normal', 'Normal'),
    ]
    PAYMENT_CHOICES = [
        ('card', 'CreditCard'),
        ('cash', 'Cash'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30)
    address = models.CharField(max_length=70)
    delivery = models.CharField(choices=DELIVERY_CHOICES, max_length=20)
    mobile = models.PositiveIntegerField()
    requirements = models.TextField(blank=True)
    total_price = models.PositiveIntegerField()

    ordered = models.BooleanField(default=False)
    payment = models.CharField(choices=PAYMENT_CHOICES, max_length=20)
    payed = models.BooleanField(default=False)
    agreed = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=30)


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='subcategories')
    name = models.CharField(max_length=30)


class Product(models.Model):
    name = models.CharField(max_length=50)
    subcategory = models.OneToOneField(Subcategory, on_delete=models.SET_NULL, null=True)
    price = models.PositiveIntegerField()
    discount_rate = models.DecimalField(max_digits=3, decimal_places=2)
    stack = models.PositiveSmallIntegerField(default=99)
    image = models.ImageField()
    description = models.TextField(max_length=255)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='orderproducts', on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)


