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

    ordered_at = models.DateTimeField(auto_now_add=True)
    payment = models.CharField(choices=PAYMENT_CHOICES, max_length=20)
    is_agreed = models.BooleanField(default=False)

    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='yet')


class Category(models.Model):
    name = models.CharField(max_length=30)
    image_bk = models.ImageField(upload_to='')
    image_pp = models.ImageField(upload_to='')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='subcategories')
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=70, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products')

    price = models.PositiveIntegerField()
    unit = models.CharField(max_length=10, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    package = models.CharField(max_length=30, blank=True)
    made_in = models.CharField(max_length=30, blank=True)
    discount_rate = models.DecimalField(max_digits=3, decimal_places=2, blank=True)
    description = models.TextField(blank=True)

    sales = models.PositiveIntegerField(default=0)
    stock = models.PositiveSmallIntegerField(default=99)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['-sales', '-discount_rate', '-created_at', '-stock'])
        ]


class Image(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='')

    def __str__(self):
        return f'{self.product} {self.name}'


class Option(models.Model):
    product = models.ForeignKey(Product, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class OrderProduct(models.Model):
    user = models.ForeignKey(User, related_name='orderproducts', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, related_name='orderproducts', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orderproducts')
    option = models.ForeignKey(Option, null=True, blank=True, related_name='orderproducts', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return f'{self.product}, {self.option}, {self.quantity}'
