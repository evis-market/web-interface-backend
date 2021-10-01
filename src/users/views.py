from django.contrib.sites.shortcuts import get_current_site
from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from app.response import response_ok
from users import serializers
from users.models import User
from users.service import SignupService, UsersService


class SignupView(APIView):
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
    serializer_class = serializers.SignupRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        signup_service = SignupService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = signup_service.signup(data=serializer.validated_data)
        return response_ok({'user_id': user.id})


class SendConfirmationEmailView(APIView):
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
    serializer_class = serializers.SendConfirmationEmailRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        signup_service = SignupService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get_by_email(serializer.validated_data['email'])
        signup_service.send_confirmation_email(user)
        return response_ok()


class UserProfileView(APIView):
    """
    TODO: copy from API docs
    """
    serializer_class = serializers.UserProfileSerializer
    update_serializer = serializers.UserProfileUpdateSerializer
    permission_classes = (AllowAny,)
    users_service = UsersService()

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        return response_ok({'profile': serializer.data})

    def put(self, request, *args, **kwargs):
        serializer = self.update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.users_service.update_user_profile(user=request.user, data=serializer.validated_data)
        return response_ok()


class UserUpdatePasswordView(APIView):
    """
    TODO: copy from API docs 
    """
    update_serializer = serializers.UserPasswordUpdateSerializer
    permission_classes = (AllowAny,)
    users_service = UsersService()

    def put(self, request, *args, **kwargs):
        serializer = self.update_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.users_service.update_user_password(user=request.user, data=serializer.validated_data)
        return response_ok()


class ConfirmEmailView(APIView, UsersService):
    """
    ## Confirm email
    
    URL: `/api/v1/users/confirm_email`
   
    Method: `POST`
    
    **Request**
        {
          "email": "test@test.com",
          "secret_code": "asd134df"
        }
    
    **Successful response**
    
        HTTP status Code: 200
        {
          "status": "OK"
        }
        
    **Failed response**
    
        HTTP status Code: 405
        {
          "status": "ERR",
          "error": {
              "code": 405,
              "msg" : "invalid secret code"
          }
        }
    """
    serializer_class = serializers.SendConfirmationEmailRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        usersSvc = UsersService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = usersSvc.confirm_email(data=serializer.validated_data)
        return result


 class SendResetPasswordEmailView(APIView, UsersService):
    """
    ## Reset password by email
    
    Generates new secret_code and sends email with link to set new password.
    URL: `/api/v1/users/send_reset_password_email`
    Method: `POST`
    **Request**
        {
          "email": "test@test.com"
        }
    
    **Successful response**
    
        HTTP status Code: 200
    
        {
          "status": "OK"
        }
    **Failed response**
        HTTP status Code: 404
    
        {
          "status": "ERR",
    
          "error": {
              "code": 404,
              "msg" : "email not found"
          }
        }
    """
    serializer_class = serializers.SendConfirmationEmailRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        usersSvc = UsersService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = usersSvc.send_reset_password_email(self, data=serializer.validated_data, domain=get_current_site(request))
        return result
class SetPasswordBySecretCodeView(APIView, UsersService):
    """
    ## Set password by secret code
    Sends email with link to set new password.
    URL: `/api/v1/users/set_password_by_secret_code`
    Method: `POST`
    **Request**
        {
          "password": "new_strong_password",
          "secret_code": "asd134df"
        }
    **Successful response**
        HTTP status Code: 200
    
        {
          "status": "OK"
        }
    **Failed response**
        HTTP status Code: 405
    
        {
          "status": "ERR",
    
          "error": {
              "code": 405,
              "msg" : "invalid secret code"
          }
        }
    """
    serializer_class = serializers.SetPasswordBySecretCodeRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        usersSvc = UsersService(domain=get_current_site(request))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = usersSvc.set_password_by_secret_code(self, data=serializer.validated_data)
        return result
  