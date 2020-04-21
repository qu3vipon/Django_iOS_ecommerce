from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response

from utils.drf.excepts import InvalidOrderingException
from .models import OrderProduct, Product, Category, Subcategory, Image
from .permissions import MyCartOnly
from .serializers import CartSerializer, CartCreateSerializer, HomeProductsSerializer, CartUpdateSerializer, \
    ProductDetailSerializer, ProductOptionSerializer


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


class MainImageView(views.APIView):
    def get(self, request):
        img_qs = Image.objects.filter(name='home').values_list('image', flat=True)
        result = []
        for img in img_qs:
            result.append("https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/" + img)

        return Response(result)


class MainMDProductsView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = HomeProductsSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related(
            'images'
        ).prefetch_related(
            'subcategory__category'
        )

    def get(self, request):
        md_list = list()
        categories = Category.objects.all()
        for cat in categories:
            md_list.append(
                self.serializer_class(self.queryset.filter(subcategory__category=cat)[:6], many=True).data
            )
        return Response(md_list)


class MainAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = HomeProductsSerializer


class RecommendationAPIView(MainAPIView):
    def get_queryset(self):
        count = self.request.query_params.get('count', None)
        if count is None:
            return Product.objects.order_by('-stock')[:30]
        else:
            return Product.objects.order_by('-stock')[:int(count)]


class DiscountAPIView(MainAPIView):
    def get_queryset(self):
        count = self.request.query_params.get('count', None)
        try:
            ordering = self.kwargs['ordering']
            if ordering not in ['-created_at', '-sales', 'price', '-price']:
                raise InvalidOrderingException

            if count is None:
                return Product.objects.order_by('-discount_rate', f'{ordering}')[:30]
            else:
                return Product.objects.order_by('-discount_rate', f'{ordering}')[:int(count)]
        except KeyError:
            if count in None:
                return Product.objects.order_by('-discount_rate')[:30]
            else:
                return Product.objects.order_by('-discount_rate')[:int(count)]


class NewAPIView(MainAPIView):
    def get_queryset(self):
        count = self.request.query_params.get('count', None)
        try:
            ordering = self.kwargs['ordering']
            if ordering not in ['-sales', '-price', 'price']:
                raise InvalidOrderingException

            if count is None:
                return Product.objects.order_by('-created_at', f'{ordering}')[:30]
            else:
                return Product.objects.order_by('-created_at', f'{ordering}')[:int(count)]
        except KeyError:
            if count is None:
                return Product.objects.order_by('-created_at')[:30]
            else:
                return Product.objects.order_by('-created_at')[:int(count)]


class BestAPIView(MainAPIView):
    def get_queryset(self):
        count = self.request.query_params.get('count', None)
        try:
            ordering = self.kwargs['ordering']
            if ordering not in ['-created_at', '-sales', '-price', 'price']:
                raise InvalidOrderingException

            if count is None:
                return Product.objects.order_by('-sales', f'{ordering}')[:30]
            else:
                return Product.objects.order_by('-sales', f'{ordering}')[:int(count)]
        except KeyError:
            if count is None:
                return Product.objects.order_by('-sales')[:30]
            else:
                return Product.objects.order_by('-sales')[:int(count)]


# 서브카테고리 전체보기
class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = HomeProductsSerializer

    def get_queryset(self):
        return Category.objects.prefetch_related('subcategories__products')

    def get(self, request, *args, **kwargs):
        result = []
        sub_qs = self.get_object().subcategories.all()
        for sub in sub_qs:
            result += sub.products.all()[:2]
        return Response(HomeProductsSerializer(result, many=True).data)


# 서브카테고리 상품 목록
class SubcategoryDetailView(generics.RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = HomeProductsSerializer

    def get_queryset(self):
        return Subcategory.objects.prefetch_related('products')

    def get(self, request, *args, **kwargs):
        return Response(HomeProductsSerializer(self.get_object().products, many=True).data)


# 상품 세부설명
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    # def get(self, request, pk):
    #     return Response(ProductDetailSerializer(self.queryset.filter(id=pk), many=True).data)


# 상품의 옵션 정보
class ProductOptionView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductOptionSerializer
