from django.contrib.auth.models import AbstractUser
from django.db import models


class Mobile(models.Model):
    number = models.PositiveIntegerField()
    token = models.PositiveSmallIntegerField()


class Address(models.Model):
    address_name = models.CharField(max_length=70)
    road_address = models.CharField(max_length=70)
    zip_code = models.PositiveSmallIntegerField()


class User(AbstractUser):
    name = models.CharField(max_length=30)
    agreed = models.BooleanField(default=False)
    mobile = models.OneToOneField(Mobile, null=True, on_delete=models.CASCADE)
    address = models.OneToOneField(Address, null=True, on_delete=models.CASCADE)
