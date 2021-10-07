import jwt
from rest_framework_simplejwt.tokens import RefreshToken

from app import exceptions
from app.conf.auth import SIMPLE_JWT
from app.settings import SECRET_KEY
from users.managers import UserManager
from users.models import User


class JWTAuthService:
    """ JWT tokens authentication service """
    GRANT_TYPE_PASSWORD = 'password'
    GRANT_TYPE_REFRESH_TOKEN = 'refresh_token'

    @staticmethod
    def valid_grant_types():
        """ Returns list of valid values for grant_type field. """

        return (JWTAuthService.GRANT_TYPE_PASSWORD, JWTAuthService.GRANT_TYPE_REFRESH_TOKEN)

    def grant_jwt_token(self,
                        data: dict) -> dict:
        """ Generates JWT token by request.

        Args:
            data['grant_type'] (str): valid values are: password, refresh_token
            data['login'] (str): login for grant type "password"
            data['password'] (str): password for grant type "password"
            data['refresh_token'] (str): refresh_token for grant type "refresh_token"

        Returns:
            Token dict with "access_token", "refresh_token", "token_type" keys.
        """
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
        """ Generate JWT token by login and password.

        Args:
            login (str): login
            password (str): password

        Raises:
            exceptions.BadRequest: if login or password invalid or user not found

        Returns:
            Token dict with "access_token", "refresh_token", "token_type" keys.
        """
        try:
            user = UserManager.get_by_login(login)
        except exceptions.NotFound:
            raise exceptions.BadRequest(msg='invalid credentials')

        if not user.check_password(password):
            raise exceptions.BadRequest(msg='invalid credentials')

        return self.get_tokens_for_user(user)

    def grant_jwt_token_by_refresh_token(self,
                                         token: str) -> dict:
        """ Generate JWT token by refresh token.

        Args:
            refresh_token (str): refresh token

        Raises:
            exceptions.BadRequest: if refresh token invalid

        Returns:
            Token dict with "access_token", "refresh_token", "token_type" keys.
        """
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
        """Generate access and refresh tokens for user.

        Args:
            user (User): user requested tokens.

        Returns:
            Token dict with "access_token", "refresh_token", "token_type" keys.
        """
        refresh = RefreshToken.for_user(user)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'token_type': SIMPLE_JWT['AUTH_HEADER_TYPES'][0],
        }
