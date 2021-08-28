REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'app.exception_handlers.default_exception_handler',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
