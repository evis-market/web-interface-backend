from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
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
    TODO: copy from API docs
    """

    def post(self, request, *args, **kwargs):
        usersSvc = UsersService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_by_email(serializer.validated_data['email'])
        usersSvc.send_confirmation_email(user)
        return response_ok()


class UserProfileView(APIView):
    serializer_class = serializers.UserProfileSerializer
    update_serializer = serializers.UserProfileUpdateSerializer
    permission_classes = (AllowAny,)
    """
    TODO: copy from API docs
    """

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return response_ok({'profile': serializer.data})

    def put(self, request, *args, **kwargs):
        serializer = self.update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usersSvc = UsersService(domain=get_current_site(request))
        with transaction.atomic():
            usersSvc.update_user_profile(user=request.user, data=serializer.validated_data)
        return response_ok()


class UserPasswordView(APIView):
    update_serializer = serializers.UserPasswordUpdateSerializer
    permission_classes = (AllowAny,)
    """
    TODO: copy from API docs 
    """

    def put(self, request, *args, **kwargs):
        serializer = self.update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usersSvc = UsersService(domain=get_current_site(request))
        with transaction.atomic():
            usersSvc.update_user_password(user=request.user, data=serializer.validated_data)
        return response_ok()
