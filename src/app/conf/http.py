ROOT_URLCONF = 'app.urls'

ALLOWED_HOSTS = [
    'localhost',
    'localhost:8000',
    'evis.market',
    'www.evis.market',
]

CORS_ALLOWED_ORIGINS = [
    'https://evis.market',
]

CSRF_TRUSTED_ORIGINS = [
    'evis.market',
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
