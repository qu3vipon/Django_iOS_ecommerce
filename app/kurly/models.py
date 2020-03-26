from django.db import models

from config.settings import MEDIA_URL
from members.models import User


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('quick', 'Quick'),
        ('normal', 'Normal'),
    ]

    PAYMENT_CHOICES = [
        ('card', 'CreditCard'),
        ('mobile', 'Mobile'),
        ('others', 'Others'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30)
    address = models.CharField(max_length=70)
    delivery = models.CharField(choices=DELIVERY_CHOICES, max_length=20)
    mobile = models.PositiveIntegerField()
    requirements = models.TextField(max_length=100, blank=True)
    total_price = models.PositiveIntegerField()

    ordered = models.BooleanField(default=False)
    payment = models.CharField(choices=PAYMENT_CHOICES, max_length=20)
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
    unit = models.CharField(max_length=10)
    amount = models.CharField(max_length=30)
    package = models.CharField(max_length=30)
    discount_rate = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField(max_length=255)

    sales = models.PositiveIntegerField(default=0)
    stock = models.PositiveSmallIntegerField(default=99)
    created = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=MEDIA_URL)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='orderproducts', on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    option = models.PositiveIntegerField(blank=True, null=True)


class Option(models.Model):
    product = models.ForeignKey(Product, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
