from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from app.response import response_ok
from users.serializers import SignupSerializer
from users.service import UsersService


class SignupView(APIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)
    usersSvc = UsersService()
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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.usersSvc.signup(data=serializer.validated_data)
        return response_ok({'user_id': user.id}, http_code=status.HTTP_200_OK)
