from django.urls import path

from . import views

urlpatterns = [
    path('cart/', views.CartListView.as_view()),
    path('main/', views.MainListView.as_view()),
    path('new/', views.NewListView.as_view()),
    path('discount/', views.DiscountListView.as_view()),
    path('best/', views.BestListView.as_view()),

]
