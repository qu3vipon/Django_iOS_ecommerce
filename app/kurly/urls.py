from django.urls import path

from . import views

urlpatterns = [
    # 메인
    path('images/', views.MainImageView.as_view()),
    path('md/', views.MDProductsAPIView.as_view()),
    path('recommend/', views.RecommendationAPIView.as_view()),
    path('new/', views.NewAPIView.as_view()),
    path('new/<str:ordering>/', views.NewAPIView.as_view()),
    path('discount/', views.DiscountAPIView.as_view()),
    path('discount/<str:ordering>/', views.DiscountAPIView.as_view()),
    path('best/', views.BestAPIView.as_view()),
    path('best/<str:ordering>/', views.BestAPIView.as_view()),

    # 장바구니
    path('cart/', views.CartListCreateView.as_view()),
    path('cart/count/', views.CartCountView.as_view()),
    path('cart/<int:pk>/', views.CartDetailView.as_view()),

    # 카테고리
    path('category/', views.CategoryView.as_view()),
    path('category/<int:pk>/all/', views.CategoryAllView.as_view()),
    path('subcategory/<int:pk>/', views.SubcategoryDetailView.as_view()),

    # 상품 세부
    path('product/', views.ProductNonLoginView.as_view()),
    path('product/<int:pk>/', views.ProductDetailView.as_view()),
    path('product/<int:pk>/option/', views.ProductOptionView.as_view()),
]
