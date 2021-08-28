from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from auth.serializers import LoginSerializer
from auth.service import JWTAuthService


class GrantJWTTokenView(APIView, JWTAuthService):
    """
    URL: /api/v1/auth/jwt/grant
    METHOD: POST
    PAYLOAD: {
              "grant_type": "password",
              "login": "email_or_phone",
              "password": "user_password"
            }
    RESPONSE: {
              "status": "OK",
              "access_token": "....jwt_token_data...",
              "refresh_token": "....jwt_token_data...",
              "token_type": "Bearer"
            }
    """
    serializer_class = LoginSerializer
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.grant_jwt_token(request=request,
                                        validate_data=serializer.validated_data)
        return Response(status=status.HTTP_200_OK, data=response)
