from rest_framework import serializers


class GrantTokenSerializer(serializers.Serializer):
    """ Class representing token serializer

    Attributes:
        grant_type (str): token grant type, required, valid values: password, refresh_token
        login (str): login, required for grant type "password"
        password (str): password, required for grant type "password"
        refresh_token (str): refresh token, required for grant type "refres_token"
    """
    grant_type = serializers.CharField(required=False)
    login = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
