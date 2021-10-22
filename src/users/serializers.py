import re
from django.core.validators import EmailValidator
from rest_framework import serializers

from app import exceptions
from users.models import User


EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
WALLET_ERC_20_PATTERN = r'^0x[a-fA-F0-9]{40}$'
MIN_PASSWORD_LENGTH = 8
MIN_PHONE_LENGTH = 11
MAX_PHONE_LENGTH = 15


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'wallet_erc20', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        # TODO: привести email к нижнему регистру, сделать валидацию email (валидный email), телефона (цифры от 7шт до 15шт) # noqa: T101

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)
        self.data['email'] = self.data['email'].lower()
        if not re.fullmatch(EMAIL_PATTERN, self.data['email']):
            raise exceptions.BadRequest('The email is Invalid')
        if len(self.data['password']) < MIN_PASSWORD_LENGTH:
            raise exceptions.BadRequest(f'The password should be {MIN_PASSWORD_LENGTH} or more symbols')
        if not self.data['phone'].isdigit() or len(self.data['phone']) < MIN_PHONE_LENGTH or len(
                self.data['phone']) > MAX_PHONE_LENGTH:
            raise exceptions.BadRequest(
                f'The phone should be only digits with length from {MIN_PHONE_LENGTH} to {MAX_PHONE_LENGTH}')
        if not re.fullmatch(WALLET_ERC_20_PATTERN, self.data['wallet_erc20']):
            raise exceptions.BadRequest('The wallet ERC-20 is Invalid')


class SendConfirmationEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])


class SetPasswordBySecretCodeRequestSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    secret_code = serializers.CharField(required=True)

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)
        if len(self.data['password']) < MIN_PASSWORD_LENGTH:
            raise exceptions.BadRequest(f'The password should be {MIN_PASSWORD_LENGTH} or more symbols')


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

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)
        return True
        # TODO: FIX  # noqa: T101
        # return self.email or self.phone or self.wallet_erc20  # noqa E800


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, required=True)
