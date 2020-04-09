from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError as DRFValidationError
from rest_framework.views import exception_handler

from config import settings


def rest_exception_handler(exc, context):
    if isinstance(exc, DjangoValidationError):
        if not settings.DEBUG:
            raise exc
        if hasattr(exc, 'message_dict'):
            exc = DRFValidationError(detail={'error': exc.message_dict})
        elif hasattr(exc, 'message'):
            exc = DRFValidationError(detail={'error': exc.message})
        elif hasattr(exc, 'messages'):
            exc = DRFValidationError(detail={'error': exc.messages})

    response = exception_handler(exc, context)

    if response:
        response.data['status'] = response.status_code
        response.data['code'] = getattr(exc, 'code', getattr(exc, 'default_code', None)) or response.data['detail'].code
    return response


# Mobile
class TakenNumberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 가입된 번호입니다.'
    default_code = 'TakenNumber'


class InvalidNumberException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '해당번호로 생성된 모바일 객체가 없습니다.'
    default_code = 'InvalidNumber'


class ResendSMSException(APIException):
    status_code = status.HTTP_200_OK
    default_detail = '인증번호 재전송'
    default_code = 'ResendSMS'


class UnauthenticatedMobile(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '휴대폰 인증 필요'
    default_code = 'UnauthorizedMobileNumber'


# Auth Token
class InvalidTokenException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '토큰값이 유효하지 않습니다.'
    default_code = 'InvalidToken'


# User
class TakenUsernameException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'username이 이미 존재합니다.'
    default_code = 'TakenUsername'


class UnauthorizedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = '사용자 인증이 필요합니다.'
    default_code = 'Unauthorized'


# Product
class ProductOptionNotMatchingException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '상품과 옵션이 매칭되지 않습니다.'
    default_code = 'ProductOptionNotMatching'
