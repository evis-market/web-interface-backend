import re
from django.core.validators import EmailValidator
from django.contrib.auth import password_validation

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app import exceptions
from users.models import User


WALLET_ERC_20_PATTERN = r'^0x[a-fA-F0-9]{40}$'
MIN_PHONE_LENGTH = 11
MAX_PHONE_LENGTH = 15


class SignupRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'wallet_erc20', 'password')

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)

        password_validation.validate_password(self.data['password'])

        phone = self.data['phone'] if self.data.get('phone') else None

        if phone and not phone.isdigit():
            raise exceptions.BadRequest(f'The phone should contain only digits')

        if phone and (len(phone) < MIN_PHONE_LENGTH or len(phone) > MAX_PHONE_LENGTH):
            raise exceptions.BadRequest(
                f'The phone should have length from {MIN_PHONE_LENGTH} to {MAX_PHONE_LENGTH}'
            )

        erc20_wallet = self.data['wallet_erc20'] if self.data.get('wallet_erc20') else ''
        if erc20_wallet and not re.fullmatch(WALLET_ERC_20_PATTERN, erc20_wallet):
            raise exceptions.BadRequest('The wallet ERC-20 is Invalid')


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
        if not(data['email'] and data['phone'] and data['wallet_erc20']):
            raise ValidationError('At least one of the fields: email, phone or wallet_erc20 should be specified')
        return data


class UserPasswordUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)

    def validate(self, data):
        password = data.get('password')
        password_validation.validate_password(password)
        return data
