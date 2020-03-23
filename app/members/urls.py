from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view()),
]
