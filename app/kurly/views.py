from rest_framework import generics
from rest_framework.response import Response

from .models import OrderProduct, Product, Category, Subcategory
from .permissions import MyCartOnly
from .serializers import CartSerializer, CartCreateSerializer, HomeProductsSerializer, CartUpdateSerializer, \
    ProductDetailSerializer


# 장바구니 목록 출력 & 추가
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


# 장바구니 수량 변경
class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = CartUpdateSerializer
    permission_classes = [MyCartOnly]


# 메인 홈화면
class MainAPIView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = HomeProductsSerializer

    def get(self, request):
        md_list = list()
        categories = Category.objects.all()
        for cat in categories:
            md_list.append(
                HomeProductsSerializer(self.queryset.filter(subcategory__category=cat)[:6], many=True).data)

        return Response({
            "md": md_list,
            "recommendation": HomeProductsSerializer(self.queryset.order_by('-stock')[:8], many=True).data,
            "discount": HomeProductsSerializer(self.queryset.order_by('-discount_rate')[:8], many=True).data,
            "new": HomeProductsSerializer(self.queryset.order_by('-created_at')[:8], many=True).data,
            "best": HomeProductsSerializer(self.queryset.order_by('-sales')[:8], many=True).data,
        })


# 베스트 아이템 50개
class BestListView(generics.ListAPIView):
    queryset = Product.objects.order_by('-sales')[:50]
    serializer_class = HomeProductsSerializer


# 신상품 50개
class NewListView(generics.ListAPIView):
    queryset = Product.objects.order_by('-created_at')[:50]
    serializer_class = HomeProductsSerializer


# 알뜰상품 50개
class DiscountListView(generics.ListAPIView):
    queryset = Product.objects.order_by('-discount_rate')[:50]
    serializer_class = HomeProductsSerializer


# 서브카테고리 전체보기
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.prefetch_related('subcategories__products')
    serializer_class = HomeProductsSerializer

    def get(self, request, *args, **kwargs):
        result = []
        sub_qs = self.get_object().subcategories.all()
        for sub in sub_qs:
            result += sub.products.all()[:2]
        return Response(HomeProductsSerializer(result, many=True).data)


# 서브카테고리 상품 목록
class SubcategoryDetailView(generics.RetrieveAPIView):
    queryset = Subcategory.objects.prefetch_related('products')
    serializer_class = HomeProductsSerializer

    def get(self, request, *args, **kwargs):
        return Response(HomeProductsSerializer(self.get_object().products, many=True).data)


# 상품 세부설명
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, pk):
        return Response(ProductDetailSerializer(self.queryset.filter(id=pk), many=True).data)
