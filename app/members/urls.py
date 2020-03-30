from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserListCreateView.as_view()),
]
