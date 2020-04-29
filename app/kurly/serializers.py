from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from utils.drf.excepts import ProductOptionNotMatchingException, UnauthorizedException
from .models import OrderProduct, Option, Product, Image, Subcategory, Category


class ProductSerializer(serializers.ModelSerializer):
    discount_rate = serializers.FloatField()
    image = serializers.SerializerMethodField('get_image')

    def get_image(self, instance):
        return instance.images.get(name='thumb').image.url

    class Meta:
        model = Product
        fields = ['pk', 'name', 'price', 'discount_rate', 'image']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['pk', 'name', 'price', 'product']


class NonLoginOptionSerializer(OptionSerializer):
    product = ProductSerializer()


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['name', 'image']


# 전체 장바구니 출력
class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    option = OptionSerializer()

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'option', 'quantity']
        depth = 1

    def to_representation(self, instance):
        rep = super().to_representation(instance)

        # option이 존재할 경우, product의 price 제거
        if rep['product'] and rep['option']:
            rep['product'].pop('price')

        # option이 존재하지 않을 경우, product만 전달
        if rep['option'] is None:
            rep.pop('option')
        return rep


# 장바구니 추가
class CartCreateSerializer(serializers.ModelSerializer):
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
        if validated_data['user'].is_authenticated:
            try:
                op = OrderProduct.objects.get(product=validated_data['product'],
                                              option=validated_data['option'],
                                              user=validated_data['user'])
            except ObjectDoesNotExist:
                return super().create(validated_data)
        else:
            raise UnauthorizedException

        # 장바구니에 이미 존재하는 상품은 수량 추
        op.quantity += validated_data['quantity']
        op.save()
        return op

    def to_representation(self, instance):
        return CartSerializer(instance).data


# 장바구니 옵션/수량 업데이트
class CartUpdateSerializer(serializers.ModelSerializer):
    product = ProductSerializer
    option = OptionSerializer

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
class HomeProductsSerializer(serializers.ModelSerializer):
    thumb_image = serializers.SerializerMethodField('get_thumb_image')
    discount_rate = serializers.FloatField()

    def get_thumb_image(self, instance):
        return instance.thumb_image[0].image.url

    class Meta:
        model = Product
        fields = ['id', 'thumb_image', 'name', 'price', 'discount_rate', 'summary']


# 상품 상세설명
class ProductDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    discount_rate = serializers.FloatField()
    options = OptionSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'summary', 'price', 'discount_rate', 'unit', 'amount', 'package', 'made_in',
                  'description', 'images', 'options']


# 비로그인 장바구니용
class ProductBriefSerializer(ProductSerializer):
    option = OptionSerializer()

    class Meta:
        model = Product
        fields = ['pk', 'name', 'price', 'discount_rate', 'image', 'option']


# 상품의 옵션 정보
class ProductOptionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'options',
        ]


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = [
            'id',
            'name',
        ]


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'image_bk',
            'image_pp',
            'subcategories',
        ]
