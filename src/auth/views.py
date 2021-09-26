from rest_framework import status
from rest_framework.views import APIView

from app.response import response_ok
from auth.serializers import GrantTokenSerializer
from auth.service import JWTAuthService


class GrantJWTTokenView(APIView):
    """
    ## Authentication by email or phone

    Returns JWT access and refresh tokens.

    URL: `/api/v1/auth/jwt/grant`

    Method: `POST`

    **Request**

        {
          "grant_type": "password",
          "login": "email_or_phone",
          "password": "user_password"
        }


    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",
          "access_token": "....jwt_token_data...",
          "refresh_token": "....jwt_token_data...",
          "token_type": "Bearer"
        }

    **Failed response**

        HTTP status Code: 400

        {
          "status": "ERR",

          "error": {
              "code": 400,
              "msg": "invalid credentials"
          }
        }


    ## Refresh tokens

    Returns JWT access and refresh tokens.

    URL: `/api/v1/auth/jwt/grant`

    Method: `POST`

    **Request**

        {
          "grant_type": "refresh_token",
          "refresh_token": "....jwt_token_data..."
        }

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",
          "access_token": "....jwt_token_data...",
          "refresh_token": "....jwt_token_data...",
          "token_type": "Bearer"
        }

    **Failed response**

        HTTP status Code: 400

        {
          "status": "ERR",

          "error": {
              "code": 400,
              "msg": "invalid token"
          }
        }
    """
    serializer_class = GrantTokenSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        jwt_auth_service = JWTAuthService()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = jwt_auth_service.grant_jwt_token(data=serializer.validated_data)
        return response_ok(result)
