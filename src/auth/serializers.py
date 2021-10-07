from rest_framework import serializers


class GrantTokenSerializer(serializers.Serializer):
    """
        Class representing token serializer

        ...
        Attributes
        ----------
        grant_type : CharField
            grant type, not required
        login : CharField
            login, not required
        password : CharField
            password, not required
        refresh_token : CharField
            refresh token, not required

        """
    grant_type = serializers.CharField(required=False)
    login = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    refresh_token = serializers.CharField(required=False)
