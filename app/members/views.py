from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from .models import User, Mobile
from .permissions import MyUserInfoOnly
from .serializers import UserSerializer, UserCreateSerializer, MobileTokenCreateSerializer, \
    MobileTokenAuthenticateSerializer, MobileSerializer, CheckDuplicatesSerializer


class UserRetrieveView(generics.RetrieveAPIView):
    permission_classes = [MyUserInfoOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class AuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })


# 각종 필드 값을 중복검사하는 View
class CheckDuplicatesView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = CheckDuplicatesSerializer

    def post(self, request):
        serializer = CheckDuplicatesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'username': serializer.validated_data['username'],
        })


# 휴대폰 인증 관련
class MobileTokenCreateView(generics.CreateAPIView):
    queryset = Mobile.objects.all()
    serializer_class = MobileTokenCreateSerializer


class MobileTokenAuthenticateView(generics.GenericAPIView):
    queryset = Mobile.objects.all()
    serializer_class = MobileTokenAuthenticateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = Mobile.objects.get(number=serializer.validated_data['number'],
                                    token=serializer.validated_data['token'])
        return Response(MobileSerializer(mobile).data)
