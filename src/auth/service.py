from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException

from app.conf.auth import AUTHENTICATION_BACKENDS, SIMPLE_JWT
from users.models import User
from pprint import pprint


class JWTAuthService:
    GRANT_TYPE_CHOICES = (
        ("password", "password"),
        ("refresh_token", "refresh_token")
    )

    def grant_jwt_token(self,
                        request,
                        data: dict) -> dict:

        if 'grant_type' not in data:
            raise APIException(code=HTTP_400_BAD_REQUEST, detail='please specify grant_type, valid grant_type: password, refresh_token')

        if data['grant_type'] == 'password':
            return self.grant_jwt_token_by_password(login=data['login'], password=data['password'])

        if data['grant_type'] == 'refresh_token':
            return self.grant_jwt_token_by_refresh_token(data['refresh_token'])

        raise APIException(code=HTTP_400_BAD_REQUEST, detail='unsupported grant_type, valid grant_type: password, refresh_token')

    def grant_jwt_token_by_password(self,
                                    login: str,
                                    password: str) -> dict:
        if login.count('@'):
            user = User.objects.filter(email=login).first()
        else:
            user = User.objects.filter(phone=login).first()

        if not user or not user.check_password(password):
            raise APIException(code=status.HTTP_400_BAD_REQUEST, detail='login or password is not match')

        return self.get_tokens_for_user(user)

    def grant_jwt_token_by_refresh_token(self, refresh_token: str):
        # TODO: реализовать
        pass

    @staticmethod
    def get_tokens_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': SIMPLE_JWT['AUTH_HEADER_TYPES'][0]
        }
