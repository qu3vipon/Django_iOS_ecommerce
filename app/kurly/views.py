from django.core.exceptions import ObjectDoesNotExist
from django.db.models import OuterRef, Subquery, F, Prefetch
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response

from utils.drf.excepts import InvalidOrderingException, InvalidOptionIdException
from .models import OrderProduct, Product, Category, Subcategory, Image, Option
from .permissions import MyCartOnly
from .serializers import CartSerializer, CartCreateSerializer, HomeProductsSerializer, CartUpdateSerializer, \
    ProductDetailSerializer, ProductOptionSerializer, ProductSerializer, NonLoginOptionSerializer, CategorySerializer


# 장바구니 목록 출력 & 추가
class CartListCreateView(generics.ListCreateAPIView):
    queryset = OrderProduct.objects.all()
    permission_classes = [MyCartOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        elif self.request.method == 'POST':
            return CartCreateSerializer

    # OrderProduct(order=None) -> 장바구니
    def get_queryset(self):
        return OrderProduct.objects.filter(order=None, user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


# 장바구니 수량 변경
class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderProduct.objects.all()
    serializer_class = CartUpdateSerializer
    permission_classes = [MyCartOnly]


# 장바구니의 상품 개수
class CartCountView(views.APIView):
    def get(self, request):
        count = OrderProduct.objects.filter(user=request.user.pk).count()
        return Response(count)


class MainImageView(views.APIView):
    def get(self, request):
        img_qs = Image.objects.filter(name='home').values_list('image', flat=True)
        result = []
        for img in img_qs:
            result.append("https://wpsios-s3.s3.ap-northeast-2.amazonaws.com/media/" + img)
        return Response(result)


# Abstract View
class MainBaseAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = HomeProductsSerializer

    def get_queryset(self):
        return Product.objects.prefetch_related(
            Prefetch('images', queryset=Image.objects.filter(name='thumb'), to_attr='thumb_image')
        )


class MDProductsAPIView(MainBaseAPIView):
    def get(self, request):
        # Subquery가 될 QuerySet
        sub_products = Product.objects.filter(subcategory=OuterRef('subcategory')).order_by('pk')
        # pk가 3임을 알려주기(메모하기)
        products = self.get_queryset().annotate(
            min_pk=Subquery(sub_products.values('pk')[2:3])
        ).filter(pk__lt=F('min_pk')).order_by('pk')
        return Response(self.serializer_class(products, many=True).data)


class RecommendationAPIView(MainBaseAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        count = self.request.query_params.get('count', None)
        if count is None:
            return queryset.order_by('-stock')[:30]
        else:
            return queryset.order_by('-stock')[:int(count)]


class DiscountAPIView(MainBaseAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        count = self.request.query_params.get('count', None)
        try:
            ordering = self.kwargs['ordering']
            if ordering not in ['-created_at', '-sales', 'price', '-price']:
                raise InvalidOrderingException

            if count is None:
                return queryset.order_by('-discount_rate', f'{ordering}')[:30]
            else:
                return queryset.order_by('-discount_rate', f'{ordering}')[:int(count)]
        except KeyError:
            if count is None:
                return queryset.order_by('-discount_rate')[:30]
            else:
                return queryset.order_by('-discount_rate')[:int(count)]


class NewAPIView(MainBaseAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        count = self.request.query_params.get('count', None)
        try:
            ordering = self.kwargs['ordering']
            if ordering not in ['-sales', '-price', 'price']:
                raise InvalidOrderingException

            if count is None:
                return queryset.order_by('-created_at', f'{ordering}')[:30]
            else:
                return queryset.order_by('-created_at', f'{ordering}')[:int(count)]
        except KeyError:
            if count is None:
                return queryset.order_by('-created_at')[:30]
            else:
                return queryset.order_by('-created_at')[:int(count)]


class BestAPIView(MainBaseAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        count = self.request.query_params.get('count', None)
        try:
            ordering = self.kwargs['ordering']
            if ordering not in ['-created_at', '-sales', '-price', 'price']:
                raise InvalidOrderingException

            if count is None:
                return queryset.order_by('-sales', f'{ordering}')[:30]
            else:
                return queryset.objects.order_by('-sales', f'{ordering}')[:int(count)]
        except KeyError:
            if count is None:
                return queryset.order_by('-sales')[:30]
            else:
                return queryset.order_by('-sales')[:int(count)]


# 카테고리 기본정보
class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.order_by('id')


# 카테고리 전체보기
class CategoryAllView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = HomeProductsSerializer

    def get_queryset(self):
        return Category.objects.prefetch_related(
            Prefetch('subcategories__products__images', queryset=Image.objects.filter(name='thumb'),
                     to_attr='thumb_image')
        )

    def get(self, request, *args, **kwargs):
        result = []
        sub_qs = self.get_object().subcategories.all()
        for sub in sub_qs:
            result += sub.products.all()[:3]
        return Response(HomeProductsSerializer(result, many=True).data)


# 서브카테고리 상품 목록
class SubcategoryDetailView(generics.RetrieveAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = HomeProductsSerializer

    def get_queryset(self):
        return Subcategory.objects.prefetch_related(
            Prefetch('products__images', queryset=Image.objects.filter(name='thumb'), to_attr='thumb_image')
        )

    def get(self, request, *args, **kwargs):
        return Response(HomeProductsSerializer(self.get_object().products, many=True).data)


# 상품 세부설명
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


# 상품의 옵션 정보
class ProductOptionView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductOptionSerializer


# 비로그인 장바구니용 상품 정보
class ProductNonLoginView(generics.GenericAPIView):
    queryset = Product.objects.all()

    def get_object(self):
        product_id = self.request.query_params.get('id', None)
        option_id = self.request.query_params.get('option', None)

        if option_id is None:
            return Product.objects.get(pk=product_id)
        else:
            try:
                Option.objects.get(pk=option_id, product=product_id)
                return Option.objects.get(pk=option_id, product=product_id)
            except ObjectDoesNotExist:
                raise InvalidOptionIdException

    def get(self, request):
        option_id = self.request.query_params.get('option', None)

        if option_id is None:
            return Response(ProductSerializer(self.get_object()).data)
        else:
            return Response(NonLoginOptionSerializer(self.get_object()).data)
