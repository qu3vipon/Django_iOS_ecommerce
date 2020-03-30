from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserListSerializer, UserCreateSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserListSerializer
        elif self.request.method == 'POST':
            return UserCreateSerializer


class ObtainTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user': UserListSerializer(user).data,
        })


# 각종 필드 값을 중복검사하는 View
class CheckDuplicatesView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            User.objects.get(username=self.request.data['username'])
        except ObjectDoesNotExist:
            return Response('중복값 없음', status=status.HTTP_200_OK)

