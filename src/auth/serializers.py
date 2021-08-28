from rest_framework import serializers


class GrantTokenSerializer(serializers.Serializer):
    grant_type = serializers.CharField(required=True)
    login = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
