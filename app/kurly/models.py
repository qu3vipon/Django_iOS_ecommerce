from django.db import models

from members.models import User, Address


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('quick', '샛별배송'),
        ('normal', '일반배송'),
    ]

    PAYMENT_CHOICES = [
        ('card', '카드결제'),
        ('mobile', '휴대폰결제'),
        ('others', '기타결제'),
    ]
    STATUS_CHOICES = [
        ('yet', '배송준비중'),
        ('on', '배송중'),
        ('done', '배송완료'),
    ]
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    delivery = models.CharField(choices=DELIVERY_CHOICES, max_length=20)
    mobile = models.PositiveIntegerField()
    requirements = models.TextField(max_length=100, blank=True)
    total_price = models.PositiveIntegerField()

    ordered = models.BooleanField(default=False)
    ordered_at = models.DateTimeField()
    payment = models.CharField(choices=PAYMENT_CHOICES, max_length=20)
    payed_at = models.DateTimeField()
    agreed = models.BooleanField(default=False)

    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='yet')


class Category(models.Model):
    name = models.CharField(max_length=30)


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='subcategories')
    name = models.CharField(max_length=30)


class Product(models.Model):
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=50)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    price = models.PositiveIntegerField()
    unit = models.CharField(max_length=10)
    amount = models.CharField(max_length=30)
    package = models.CharField(max_length=30)
    discount_rate = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField(max_length=255)

    sales = models.PositiveIntegerField(default=0)
    stock = models.PositiveSmallIntegerField(default=99)
    created_at = models.DateTimeField(auto_now_add=True)


class Image(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='')


class Option(models.Model):
    product = models.ForeignKey(Product, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='orderproducts', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderproducts')
    option = models.ForeignKey(Option, blank=True, null=True, related_name='orderproducts', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
