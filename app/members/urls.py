from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>/', views.UserDetailView.as_view()),
    path('', views.UserCreateView.as_view()),
    path('duplicates/', views.CheckDuplicatesView.as_view()),
    path('m-token-create/', views.MobileTokenCreateView.as_view()),
    path('m-token-auth/', views.MobileTokenAuthenticateView.as_view()),
    path('auth-token/', views.AuthTokenView.as_view()),
]
