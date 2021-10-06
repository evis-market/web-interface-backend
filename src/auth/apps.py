from django.apps import AppConfig


class AuthConfig(AppConfig):
    """
        Class representing authorization and its configuration

        ...
        Attributes
        ----------
        default_auto_field : str
            default auto field
        name : str
            authorization name
        label : str
            label of authorization

        """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
    label = 'app_auth'
