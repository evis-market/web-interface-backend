import jwt
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import APIException

from app.conf.auth import SIMPLE_JWT
from app.settings import SECRET_KEY
from users.models import User


class GrantTypes:
    password = 'password'
    refresh_token = 'refresh_token'


class JWTAuthService:

    def grant_jwt_token(self,
                        data: dict) -> dict:
        if 'grant_type' not in data:
            raise APIException(code=status.HTTP_400_BAD_REQUEST, detail='please specify grant_type, valid grant_type: password, refresh_token')

        if data['grant_type'] == GrantTypes.password:
            return self.grant_jwt_token_by_password(login=data['login'], password=data['password'])

        if data['grant_type'] == GrantTypes.refresh_token:
            return self.grant_jwt_token_by_refresh_token(data['refresh_token'])

        raise APIException(code=status.HTTP_400_BAD_REQUEST, detail='unsupported grant_type, valid grant_type: password, refresh_token')

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

    def grant_jwt_token_by_refresh_token(self,
                                         token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=SIMPLE_JWT['ALGORITHM'])
        except Exception:
            raise APIException(code=status.HTTP_400_BAD_REQUEST, detail='Authentication error. Unable to decode token')
        try:
            user = User.objects.get(uuid=payload['user_id'])
        except User.DoesNotExist:
            raise APIException(code=status.HTTP_400_BAD_REQUEST, detail='No user matching this token was found')
        return self.get_tokens_for_user(user)

    @staticmethod
    def get_tokens_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': SIMPLE_JWT['AUTH_HEADER_TYPES'][0]
        }
