from django.urls import path

from . import views

urlpatterns = [
    # 메인
    path('images/', views.MainImageView.as_view()),
    path('md/', views.MainMDProductsView.as_view()),
    path('recommend/', views.RecommendationAPIView.as_view()),
    path('new/', views.NewAPIView.as_view()),
    path('discount/', views.DiscountAPIView.as_view()),
    path('best/', views.BestAPIView.as_view()),

    # 장바구니
    path('cart/', views.CartListCreateView.as_view()),
    path('cart/<int:pk>/', views.CartDetailView.as_view()),

    # 카테고리
    path('category/<int:pk>/', views.CategoryDetailView.as_view()),
    path('subcategory/<int:pk>/', views.SubcategoryDetailView.as_view()),

    # 상품 세부
    path('product/<int:pk>/', views.ProductDetailView.as_view()),
    path('product/<int:pk>/option/', views.ProductOptionView.as_view()),
]
