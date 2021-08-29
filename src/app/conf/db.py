from app.conf.environ import env

DATABASES = {
    'default': env.db(),
}

if not env('DEBUG', cast=bool):
    DATABASES['default']['CONN_MAX_AGE'] = 600
