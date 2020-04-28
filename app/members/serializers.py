import random
import string

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from utils.drf.coolsms import coolsms
from utils.drf.excepts import InvalidNumberException, TakenNumberException, InvalidTokenException, \
    TakenUsernameException, ResendSMSException, UnauthenticatedMobile
from utils.drf.serializers import ModelSerializer
from .models import User, Mobile, Address


# Mobile
class MobileSerializer(ModelSerializer):
    class Meta:
        model = Mobile
        fields = ['number', 'is_authenticated']


class MobileTokenCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ['number', 'token']
        read_only_fields = ['token']

    def validate_number(self, value):
        try:
            mobile = Mobile.objects.get(number=value)
        except ObjectDoesNotExist:
            return value

        if mobile.is_authenticated:
            try:
                User.objects.get(mobile=mobile)
            except ObjectDoesNotExist:
                self.sms_new_token(mobile)
                raise ResendSMSException
            raise TakenNumberException
        else:
            self.sms_new_token(mobile)
            raise ResendSMSException

    def create(self, validated_data):
        mobile = Mobile.objects.create(number=validated_data['number'])
        self.sms_new_token(mobile)
        return mobile

    @staticmethod
    def sms_new_token(mobile):
        mobile.token = ''.join(random.choices(string.digits, k=6))
        mobile.save()
        coolsms(mobile)


class MobileTokenAuthenticateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mobile
        fields = ['number', 'token']

    def validate(self, data):
        try:
            mobile = Mobile.objects.get(number=data['number'])
        except ObjectDoesNotExist:
            raise InvalidNumberException

        if mobile.token == data['token']:
            mobile.is_authenticated = True
            mobile.save()
        else:
            raise InvalidTokenException
        return data


class CheckDuplicatesSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
            raise TakenUsernameException
        except ObjectDoesNotExist:
            return value


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
        fields = ['id', 'email', 'username', 'name', 'mobile', 'address', 'birth_date', 'gender', 'last_login']


class UserCreateSerializer(serializers.ModelSerializer):
    mobile = PhoneNumberField()
    address = serializers.DictField(child=serializers.CharField())

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password', 'mobile', 'address', 'birth_date', 'gender']

    def validate_mobile(self, value):
        try:
            mobile = Mobile.objects.get(number=value)
        except ObjectDoesNotExist:
            raise InvalidNumberException

        if mobile.is_authenticated:
            return mobile
        else:
            raise UnauthenticatedMobile

    def create(self, validated_data):
        validated_data['address'], _ = Address.objects.get_or_create(
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
