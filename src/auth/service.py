import jwt
from rest_framework_simplejwt.tokens import RefreshToken

from app import exceptions
from app.conf.auth import SIMPLE_JWT
from app.settings import SECRET_KEY
from users.managers import UserManager
from users.models import User


class JWTAuthService:
    GRANT_TYPE_PASSWORD = 'password'
    GRANT_TYPE_REFRESH_TOKEN = 'refresh_token'

    @staticmethod
    def valid_grant_types():
        return (JWTAuthService.GRANT_TYPE_PASSWORD, JWTAuthService.GRANT_TYPE_REFRESH_TOKEN)

    def grant_jwt_token(self,
                        data: dict) -> dict:
        if 'grant_type' not in data:
            raise exceptions.BadRequest(
                msg='please specify grant_type, valid grant_type: ' + ', '.join(JWTAuthService.valid_grant_types()))

        if data['grant_type'] == JWTAuthService.GRANT_TYPE_PASSWORD:
            return self.grant_jwt_token_by_password(login=data.get('login', None), password=data.get('password', None))

        if data['grant_type'] == JWTAuthService.GRANT_TYPE_REFRESH_TOKEN:
            return self.grant_jwt_token_by_refresh_token(data.get('refresh_token', None))

        raise exceptions.BadRequest(
            msg='please specify grant_type, valid grant_type: ' + ', '.join(JWTAuthService.valid_grant_types()))

    def grant_jwt_token_by_password(self,
                                    login: str,
                                    password: str) -> dict:
        try:
            user = UserManager.get_by_login(login)
        except User.DoesNotExist:
            raise exceptions.BadRequest(msg='invalid credentials')
        if not user.check_password(password):
            raise exceptions.BadRequest(msg='invalid credentials')

        return self.get_tokens_for_user(user)

    def grant_jwt_token_by_refresh_token(self,
                                         token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=SIMPLE_JWT['ALGORITHM'])
        except Exception:
            raise exceptions.BadRequest(msg='invalid token')
        try:
            user = User.objects.get(uuid=payload['user_id'])
        except User.DoesNotExist:
            raise exceptions.BadRequest(msg='invalid token')

        return self.get_tokens_for_user(user)

    @staticmethod
    def get_tokens_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': SIMPLE_JWT['AUTH_HEADER_TYPES'][0],
        }
