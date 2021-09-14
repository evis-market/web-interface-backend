from app.conf.environ import env


DEFAULT_FROM_EMAIL = 'EVIS <no-reply@evis.market>'
SERVER_EMAIL = 'EVIS <no-reply@evis.market>'
EMAIL_HOST = '127.0.0.1'
EMAIL_PORT = '25'
ADMINS = (('Evgeny Mamonov', 'evgeny@mamonov.org'), )

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if env('DEBUG', cast=bool):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
