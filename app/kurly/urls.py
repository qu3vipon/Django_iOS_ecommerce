from django.urls import path

from . import views

urlpatterns = [
    path('main/', views.MainAPIView.as_view()),
    path('new/', views.NewListView.as_view()),
    path('discount/', views.DiscountListView.as_view()),
    path('best/', views.BestListView.as_view()),
    path('cart/', views.CartListCreateView.as_view()),
    path('cart/<int:pk>/', views.CartDetailView.as_view()),
]