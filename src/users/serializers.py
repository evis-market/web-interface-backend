from django.core.validators import EmailValidator
from rest_framework import serializers

from users.models import User


class SignupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'wallet_erc20', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        # TODO: привести email к нижнему регистру, сделать валидацию email (валидный email), телефона (цифры от 7шт до 15шт)


class SendConfirmationEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, validators=[EmailValidator])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'wallet_erc20')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    wallet_for_payments_erc20 = serializers.CharField(required=False)

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception)
        return self.email or self.phone or self.wallet_for_payments_erc20
