from app.conf.environ import env


ROOT_URLCONF = 'app.urls'

DEBUG = env('DEBUG', cast=bool)

APPEND_SLASH=False

ALLOWED_HOSTS = [
    'evis.market',
]

if DEBUG:
    ALLOWED_HOSTS += [
        'localhost',
        'localhost:8000',
        'evis.market:8000',
        'dev.evis.market',
    ]

CORS_ALLOWED_ORIGINS = [
    'https://evis.market',
]

if DEBUG:
    CORS_ALLOWED_ORIGINS += [
        'http://evis.market:8000',
        'http://dev.evis.market',
    ]

CSRF_TRUSTED_ORIGINS = [
    'evis.market',
]

if DEBUG:
    CSRF_TRUSTED_ORIGINS += [
        'evis.market:8000',
        'dev.evis.market',
    ]

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = False  # service installed behind reverse proxy, no https needed
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
