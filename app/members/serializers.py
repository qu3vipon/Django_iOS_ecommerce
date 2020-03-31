from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Mobile, Address


# Mobile
class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ['number', 'is_authenticated']


class MobileTokenCreateSerializer(serializers.ModelSerializer):
    number = serializers.CharField()

    class Meta:
        model = Mobile
        fields = ['number', 'token']


# Address
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_name', 'road_address', 'zip_code']


# User
class UserSerializer(serializers.ModelSerializer):
    mobile = MobileSerializer()
    address = AddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'mobile', 'address', 'birth_date', 'gender', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField()
    address = serializers.DictField(child=serializers.CharField())

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password', 'mobile', 'address', 'birth_date', 'gender']

    def create(self, validated_data):
        mobile = Mobile.objects.get(number=validated_data['mobile'])
        if mobile.is_authenticated:
            validated_data['mobile'] = mobile

        validated_data['address'], created = Address.objects.get_or_create(
            address_name=validated_data['address']['address_name'],
            road_address=validated_data['address']['road_address'],
            zip_code=validated_data['address']['zip_code'])
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        return UserSerializer(instance).data


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
