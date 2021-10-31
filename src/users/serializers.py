from django.core.validators import EmailValidator
from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app import exceptions
from app.validators import PhoneValidator, ERC20Validator
from users import models
from users.models import User



class SignupRequestSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False, validators=[PhoneValidator])
    email = serializers.EmailField(required=False, validators=[EmailValidator])
    wallet_erc20 = serializers.CharField(required=False, validators=[ERC20Validator])
    password = serializers.CharField(required=True)

    def validate(self, data):
        if not (data['email'] and data['phone'] and data['wallet_erc20']):
            raise ValidationError('At least one of the fields: email, phone or wallet_erc20 should be specified')
        return data


class SendConfirmationEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])


class ConfirmEmailViewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])
    secret_code = serializers.CharField(required=True)


class SetPasswordBySecretCodeRequestSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    secret_code = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)
        password_validation.validate_password(self.data['password'])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'wallet_erc20')


class UserProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    wallet_erc20 = serializers.CharField(required=False)

    def validate(self, data):
        if not (data['email'] and data['phone'] and data['wallet_erc20']):
            raise ValidationError('At least one of the fields: email, phone or wallet_erc20 should be specified')
        return data


class UserPasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get('password')
        password_validation.validate_password(password)
        return data
