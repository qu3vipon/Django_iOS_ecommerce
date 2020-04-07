from rest_framework import generics

from .models import OrderProduct
from .permissions import MyCartOnly
from .serializers import CartSerializer, CartCreateSerializer


# 장바구니 목록 출력
class CartListCreateView(generics.ListCreateAPIView):
    queryset = OrderProduct.objects.all()
    permission_classes = [MyCartOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CartCreateSerializer

    # OrderProduct(order = None) -> 장바구니
    def get_queryset(self):
        return OrderProduct.objects.filter(order=None)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
