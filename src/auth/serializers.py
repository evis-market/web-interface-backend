from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    grant_type = serializers.CharField(required=True)
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
