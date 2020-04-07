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
        fields = ['product', 'option', 'quantity']

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # option이 존재할 경우, option만 전달
        if rep['product'] and rep['option']:
            rep.pop('product')

        # option이 존재하지 않을 경우, product만 전달
        if rep['option'] is None:
            rep.pop('option')
        return rep


# 장바구니 추가
class CartCreateSerializer(serializers.ModelSerializer):
    product = ProductBasicSerializer
    option = OptionBasicSerializer

    class Meta:
        model = OrderProduct
        fields = ['product', 'option', 'quantity']

    def validate(self, data):
        # 옵션이 존재할 경우, 상품과 옵션이 일치하는지 확인
        if data['option']:
            if data['option'].product != data['product']:
                raise ProductOptionNotMatchingException
        return data

    def to_representation(self, instance):
        return CartSerializer(instance).data
