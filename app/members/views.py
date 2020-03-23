from rest_framework import generics, permissions

from .models import User
from .serializers import UserListSerializer, UserCreateSerializer


class UserListView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif self.request.method == 'POST':
            return UserCreateSerializer

