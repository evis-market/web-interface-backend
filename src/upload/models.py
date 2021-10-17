import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible

from upload.managers import UploadedFileManager


@deconstructible
class PathAndRename:

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        filename = f'{uuid.uuid4().hex}.{filename.split(".")[-1]}'
        return os.path.join(self.path, filename)


class UploadedFile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=PathAndRename('uploaded_files_tmp/'))  # noqa: VNE002
    file_name_original = models.CharField(max_length=255)
    created_by = models.ForeignKey('users.User', related_name='upload_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    objects = UploadedFileManager()

    class Meta:
        db_table = 'uploaded_files'
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.file_name_original = self.file.name
        super().save(force_insert, force_update, using, update_fields)

    @property
    def get_filename_without_extension(self):
        return os.path.basename(self.file.name).split('.')[0]

    @property
    def get_filename_extension(self):
        return os.path.basename(self.file.name).split('.')[-1]

    def __str__(self):
        return f'{self.uuid}-{self.file}'
