from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, Mobile, Address


class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ['number']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_name', 'road_address', 'zip_code']


class UserListSerializer(serializers.ModelSerializer):
    mobile = MobileSerializer()
    address = AddressSerializer()

    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField()
    address = serializers.DictField(child=serializers.CharField())

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'mobile', 'address', 'birth_date', 'gender']

    def create(self, validated_data):
        validated_data['mobile'], created = Mobile.objects.get_or_create(number=validated_data['mobile'])
        if not created:
            raise ValueError('휴대폰 번호 중복')
        validated_data['address'], created = Address.objects.get_or_create(
            address_name=validated_data['address']['address_name'],
            road_address=validated_data['address']['road_address'],
            zip_code=validated_data['address']['zip_code'])
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        return UserListSerializer(instance).data


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
