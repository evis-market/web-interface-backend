from django.db import models
from upload.managers import UploadedFileManager


class UploadedFile(models.Model):
    uuid = models.UUIDField(primary_key=True)
    file_path = models.FileField(upload_to='tmp/uploaded_files/')
    model = models.CharField(max_length=255)
    model_field = models.CharField(max_length=255)
    created_by = models.ForeignKey('users.User', related_name='upload_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    objects = UploadedFileManager()
