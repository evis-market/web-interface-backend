from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from app.conf.auth import AUTHENTICATION_BACKENDS, SIMPLE_JWT
from users.models import User


class LoginUserService:

    def grant_token(self,
                    request,
                    validate_data: dict) -> dict:
        if validate_data['grant_type'] == 'password':
            user, tokens = self.auth_by_password(login_data=validate_data['login'],
                                                 password=validate_data['password'])
            login(request, user, backend=AUTHENTICATION_BACKENDS[0])
            return tokens

    def auth_by_password(self,
                         login_data: str,
                         password: str) -> (User, dict):
        if login_data.count('@'):
            user = User.objects.filter(email=login_data).first()
        else:
            user = User.objects.filter(phone=login_data).first()
        if user and user.check_password(password):
            authenticate(uuid=user.uuid, password=password)
            return user, self.get_tokens_for_user(user)

    @staticmethod
    def get_tokens_for_user(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': SIMPLE_JWT['AUTH_HEADER_TYPES'][0]
        }
