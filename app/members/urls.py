from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserListCreateView.as_view()),
    path('duplicates/', views.CheckDuplicatesView.as_view()),
    path('m-token-create/', views.MobileTokenCreateView.as_view()),
    path('m-token-auth/', views.MobileTokenAuthenticateView.as_view()),
]
