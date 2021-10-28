import os

from app.conf.environ import env
from app.settings import BASE_DIR


MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
MEDIA_URL = '/media/'
