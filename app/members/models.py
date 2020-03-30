from django.contrib.auth.models import AbstractUser
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Mobile(models.Model):
    number = PhoneNumberField()
    token = models.PositiveSmallIntegerField(null=True, blank=True)
    authenticated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.number}'


class Address(models.Model):
    address_name = models.CharField(max_length=70)
    road_address = models.CharField(max_length=70)
    zip_code = models.CharField(max_length=10)  # 카카오 주소 api 우편번호 type: string

    def __str__(self):
        return f'address_name: {self.address_name}, road_address: {self.road_address}, zip_code: {self.zip_code}'


class User(AbstractUser):
    GENDER_CHOICES = [
        ('m', 'Male'),
        ('f', 'Female'),
        ('n', 'None'),
    ]
    email = models.EmailField()
    name = models.CharField(max_length=30)
    agreed = models.BooleanField(default=False)
    mobile = models.OneToOneField(Mobile, on_delete=models.CASCADE, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='n')

    def __str__(self):
        return f'username: {self.username}, email: {self.email}, name" {self.name}, mobile: {self.mobile}, address: {self.address}'
