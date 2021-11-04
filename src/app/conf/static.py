import os

from app.conf.environ_app import env
from app.settings import BASE_DIR


STATIC_URL = env('STATIC_URL', cast=str, default='/static/')
STATIC_ROOT = os.path.join(BASE_DIR, '../static')
