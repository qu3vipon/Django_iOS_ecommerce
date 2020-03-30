import random
import string

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Mobile
from .serializers import UserListSerializer, UserCreateSerializer, MobileTokenCreateSerializer
from .utils import coolsms


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
            return Response('중복값 없음')


class MobileTokenCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MobileTokenCreateSerializer(data=self.request.data)
        if serializer.is_valid():
            mobile, created = Mobile.objects.get_or_create(number=serializer.validated_data['number'])
            if not created:
                if mobile.authenticated:
                    raise ValueError('이미 가입된 전화번호입니다.')
                raise ValueError('인증되지 않은 동일한 번호가 존재합니다.')
            mobile.token = ''.join(random.choices(string.digits, k=4))
            mobile.save()
            coolsms(mobile)
            return Response('토큰 전송 완료')
        return Response('전화번호를 올바르게 입력해주세요.', status=status.HTTP_400_BAD_REQUEST)


class MobileTokenAuthenticateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MobileTokenCreateSerializer(data=self.request.data)
        if serializer.is_valid():
            try:
                mobile = Mobile.objects.get(number=serializer.validated_data['number'], token=serializer.validated_data['token'])
                mobile.authenticated = True
                mobile.save()
            except ValueError:
                return Response('인증 실패', status=status.HTTP_401_UNAUTHORIZED)
            return Response('휴대폰 인증 완료')
