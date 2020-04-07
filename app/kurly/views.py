from rest_framework import generics
from rest_framework.response import Response

from .models import OrderProduct, Order, Product, Category
from .permissions import MyCartOnly
from .serializers import CartListSerializer, CartCreateSerializer, HomeSerializer


# 장바구니 생성
class CartCreateView(generics.CreateAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = CartCreateSerializer()


# 장바구니 목록 출력
class CartListView(generics.ListAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = CartListSerializer
    permission_classes = [MyCartOnly]

    # OrderProduct(order = None) -> 장바구니
    def get_queryset(self):
        return OrderProduct.objects.filter(order=None)


# 메인 홈화면
class MainListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = HomeSerializer

    def md(self):
        result = {}
        categories = Category.objects.all()
        for cat in categories:
            key = cat.name
            result[key] = HomeSerializer(self.queryset.filter(subcategory__category__name=key)[:6], many=True).data
        return result

    def list(self, request):
        return Response({
            "md": self.md(),
            "recommendation": HomeSerializer(self.queryset.order_by('-stock')[:8], many=True).data,
            "discount": HomeSerializer(self.queryset.order_by('-discount_rate')[:8], many=True).data,
            "new": HomeSerializer(self.queryset.order_by('-created_at')[:8], many=True).data,
            "best": HomeSerializer(self.queryset.order_by('-sales')[:8], many=True).data,
        })


# 베스트 아이템 50개
class BestListView(generics.ListAPIView):
    queryset = Product.objects.order_by('-sales')[:50]
    serializer_class = HomeSerializer


# 신상품 50개
class NewListView(generics.ListAPIView):
    queryset = Product.objects.order_by('-created_at')[:50]
    serializer_class = HomeSerializer


# 알뜰상품 50개
class DiscountListView(generics.ListAPIView):
    queryset = Product.objects.order_by('-discount_rate')[:50]
    serializer_class = HomeSerializer


