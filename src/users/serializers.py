from rest_framework import serializers

from users.models import User


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'wallet_erc20')
        extra_kwargs = {'password': {'write_only': True}}
        # TODO: привести email к нижнему регистру, сделать валидацию email (валидный email), телефона (цифры от 7шт до 15шт)
