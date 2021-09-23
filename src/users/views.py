from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from app.response import response_ok
from users import serializers
from users.models import User
from users.service import UsersService


class SignupView(APIView):
    serializer_class = serializers.SignupRequestSerializer
    permission_classes = (AllowAny,)
    """
    ## Signup by email or phone

    URL: `/api/v1/users/signup`

    Method: `POST`

    **Request**

        {
          "first_name": "Evgeny",
          "last_name": "Mamonov",
          "phone": "15552223456",
          "email": "test@test.com",
          "password": "some_very_strong_password"
        }

    **Required fields**
    * phone or email (one of)
    * password

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",
          "user_id": 1
        }

    **Failed response**

        HTTP status Code: 405

        {
          "status": "ERR",

          "error": {
              "code": 405,

              "invalid_fields": {
                "email": "invalid format",
                "password": "too short, 8 symbols minimum"
              },

              "msg" : "bad request"
          }
        }
    """
    def post(self, request, *args, **kwargs):
        usersSvc = UsersService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = usersSvc.signup(data=serializer.validated_data)
        return response_ok({'user_id': user.id})


class SendConfirmationEmailView(APIView):
    serializer_class = serializers.SendConfirmationEmailRequestSerializer
    permission_classes = (AllowAny,)
    """
    ## Generates new secret_code and sends email with link to confirm email.

    URL: `/api/v1/users/send_email_confirmation`

    Method: `POST`

    **Request**

        {
          "email": "test@test.com"
        }

    **Successful response**

        {
          "status": "OK",
        }

    **Failed response**

        HTTP status Code: 400

        {
          "status": "ERR",

          "error": {
              "code": 400,
              "msg": "email not found"
          }
        }
    """
    def post(self, request, *args, **kwargs):
        usersSvc = UsersService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_by_email(serializer.validated_data['email'])
        usersSvc.send_confirmation_email(user)
        return response_ok()
