from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from app.conf.auth import AUTHENTICATION_BACKENDS, SIMPLE_JWT
from users.models import User


class JWTAuthService:

    def grant_jwt_token(self,
                        request,
                        validate_data: dict) -> dict:

        if validate_data['grant_type'] == 'password':
            user, tokens = self.grant_jwt_token_by_password(login=validate_data['login'],
                                                 password=validate_data['password'])
            login(request, user, backend=AUTHENTICATION_BACKENDS[0])
            return tokens

        if validate_data['grant_type'] == 'refresh_token':
            # TODO: реализовать
            pass

        # TODO: http status code: 405, error code 405, error message: unsupported grant_type, valid grant_type: password, refresh_token
        # по хорошему взять данные для valid grant_type из GRANT_TYPE_CHOICES, или убрать GRANT_TYPE_CHOICES

    def grant_jwt_token_by_password(self,
                         login: str,
                         password: str) -> (User, dict):
        if login.count('@'):
            user = User.objects.filter(email=login).first()
        else:
            user = User.objects.filter(phone=login).first()
        if user and user.check_password(password):
            authenticate(uuid=user.uuid, password=password)
            return user, self.get_tokens_for_user(user)

    def grant_jwt_token_by_refresh_token(self):
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
