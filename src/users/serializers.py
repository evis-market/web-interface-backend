from django.core.validators import EmailValidator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app import exceptions
from app.validators import PhoneValidator, ERC20Validator, PasswordValidator
from users.models import User


LOGIN_NOT_SET_ERR_MSG = 'At least one of the fields: email, phone or wallet_erc20 should be specified'

def is_login_field_exists(data):
    if 'email' in data and data['email']:
        return True

    if 'phone' in data and data['phone']:
        return True

    if 'wallet_erc20' in data and data['wallet_erc20']:
        return True

    return False


class SignupRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, validators=[PhoneValidator])
    email = serializers.EmailField(required=False, validators=[EmailValidator])
    wallet_erc20 = serializers.CharField(required=False, validators=[ERC20Validator])
    password = serializers.CharField(required=True, validators=[PasswordValidator])

    def validate(self, data):
        if not is_login_field_exists(data):
            raise exceptions.BadRequest(LOGIN_NOT_SET_ERR_MSG)

        if 'phone' in data:
            if User.objects.filter(phone=data['phone']).count() > 0:
                raise ValidationError({"phone": "user with this phone already exists"})

        if 'email' in data:
            if User.objects.filter(email=data['email']).count() > 0:
                raise ValidationError({"email": "user with this email already exists"})

        if 'wallet_erc20' in data:
            if User.objects.filter(wallet_erc20=data['wallet_erc20']).count() > 0:
                raise ValidationError({"wallet_erc20": "user with this wallet already exists"})


        return data



class SendConfirmationEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])


class ConfirmEmailViewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    secret_code = serializers.CharField(required=True)


class SetPasswordBySecretCodeRequestSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, validators=[PasswordValidator])
    secret_code = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'wallet_erc20')


class UserProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, validators=[PhoneValidator])
    email = serializers.EmailField(required=False, validators=[EmailValidator])
    wallet_erc20 = serializers.CharField(required=False, validators=[ERC20Validator])

    def validate(self, data):
        if not is_login_field_exists(data):
            raise exceptions.BadRequest(LOGIN_NOT_SET_ERR_MSG)

        return data


class UserPasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, validators=[PasswordValidator])
