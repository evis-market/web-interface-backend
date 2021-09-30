import uuid

from django.db import models
from upload.managers import UploadedFileManager


class UploadedFile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_path = models.FileField(upload_to='uploaded_tmp/')
    file_name_original = models.CharField(max_length=255)
    created_by = models.ForeignKey('users.User', related_name='upload_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    objects = UploadedFileManager()

    class Meta:
        db_table = 'uploaded_files'
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'
