import os

from app.conf.environ_app import env
from app.settings import BASE_DIR


MEDIA_ROOT = os.path.join(BASE_DIR, '../media')
MEDIA_URL = '/media/'
if 'FILE_UPLOAD_PERMISSIONS' not in env:
    FILE_UPLOAD_PERMISSIONS = 436
else:
    FILE_UPLOAD_PERMISSIONS = int(env('FILE_UPLOAD_PERMISSIONS'))
    FILE_UPLOAD_PERMISSIONS = FILE_UPLOAD_PERMISSIONS
