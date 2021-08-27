from rest_framework import serializers


class LoginSerializer(serializers.Serializer):

    GRANT_TYPE_CHOICES = (
        ("password", "password"),
        ("refresh_token", "refresh_token")
    )

    grant_type = serializers.ChoiceField(choices=GRANT_TYPE_CHOICES, required=True)
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
