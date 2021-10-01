import uuid
import os
from django.db import models
from upload.managers import UploadedFileManager
from product_data_types.models import DataFormat, DataType
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename:

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        filename = f'{uuid.uuid4().hex}.{filename.split(".")[-1]}'
        path = os.path.join(self.path, filename)
        return path


# path_and_rename = PathAndRename("uploaded_tmp/")


class UploadedFile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_path = models.FileField(upload_to=PathAndRename("uploaded_tmp/"))
    file_name_original = models.CharField(max_length=255)  # todo: set on runtime
    data_type = models.ForeignKey(DataType, blank=True, null=True, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, blank=True, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey('users.User', related_name='upload_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    objects = UploadedFileManager()

    class Meta:
        db_table = 'uploaded_files'
        verbose_name = 'Uploaded File'
        verbose_name_plural = 'Uploaded Files'
