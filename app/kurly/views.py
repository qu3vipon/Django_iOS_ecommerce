from rest_framework import generics
from rest_framework.response import Response

from .models import OrderProduct
from .permissions import MyCartOnly
from .serializers import CartListSerializer, CartCreateSerializer


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
