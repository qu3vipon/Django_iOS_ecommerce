from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from utils.drf.excepts import ProductOptionNotMatchingException
from .models import OrderProduct, Option, Product


class ProductBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'price']


class OptionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['pk', 'name', 'price', 'product']


# 전체 장바구니 출력
class CartSerializer(serializers.ModelSerializer):
    product = ProductBasicSerializer()
    option = OptionBasicSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'option', 'quantity']

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # option이 존재할 경우, option만 전달
        if rep['product'] and rep['option']:
            rep.pop('product')

        # option이 존재하지 않을 경우, product만 전달
        if rep['option'] is None:
            rep.pop('option')
        return rep


# 장바구니 추
class CartCreateSerializer(serializers.ModelSerializer):
    product = ProductBasicSerializer
    option = OptionBasicSerializer

    class Meta:
        model = OrderProduct
        fields = ['product', 'option', 'quantity']

    def validate(self, data):
        # 옵션이 존재할 경우
        if data['option']:
            # 상품과 옵션 일치 확인
            if data['option'].product != data['product']:
                raise ProductOptionNotMatchingException
        return data

    def create(self, validated_data):
        try:
            op = OrderProduct.objects.get(product=validated_data['product'], option=validated_data['option'])
        except ObjectDoesNotExist:
            return super().create(validated_data)

        # 장바구니에 이미 존재하는 상품은 수량 추
        op.quantity += validated_data['quantity']
        op.save()
        return op

    def to_representation(self, instance):
        return CartSerializer(instance).data


# 장바구니 옵션/수량 업데이트
class CartUpdateSerializer(serializers.ModelSerializer):
    product = ProductBasicSerializer
    option = OptionBasicSerializer

    class Meta:
        model = OrderProduct
        fields = ['product', 'option', 'quantity']

    def validate(self, data):
        if data['option']:
            if data['option'].product != data['product']:
                raise ProductOptionNotMatchingException
        return data

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.option = validated_data.get('option', instance.option)
        instance.save()
        return instance

    def to_representation(self, instance):
        return CartSerializer(instance).data


# 홈 화면
class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount_rate', 'summary']
