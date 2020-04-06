from rest_framework import serializers

from .models import OrderProduct, Option, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'price']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['pk', 'name', 'price', 'product']


# 장바구니
class CartCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['']


class CartListSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    option = OptionSerializer()

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


# class OrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ['receiver', 'address', 'delivery', 'mobile', 'requirements', 'total_price', 'payment', 'ordered_at']
#

class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'discount_rate', 'summary']