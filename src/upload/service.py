import os
import shutil
import hashlib

from django.core.exceptions import ObjectDoesNotExist
from app import exceptions
from app.conf.base import MEDIA_ROOT
from upload.models import UploadedFile


class UploadService:
    BUFFER_SIZE = 1000
    NOTFOUND_UPLOADED_FILE_MSG = 'File does not exist or you do not have access permissions to it'
    INCORRECT_FILE_COPYING = 'File from source destination copied incorrectly'
    TMP_FILE_NOT_FOUND = 'File not found in temp directory'

    def get_object(self, uuid, created_by):
        uploaded_file = UploadedFile.objects.get_by_uuid_and_author(uuid, created_by)
        if not uploaded_file:
            raise exceptions.NotFound(msg=self.NOTFOUND_UPLOADED_FILE_MSG)
        return uploaded_file

    def create_object(self, data):
        return UploadedFile.objects.create(**data)

    def _get_file_hash(self, file_path):
        file_hash = hashlib.sha256()
        with open(file_path, 'rb') as fp:
            while True:
                data = fp.read(self.BUFFER_SIZE)
                if not data:
                    break
                file_hash.update(data)
        return file_hash.hexdigest()

    def copy_file_from_tmp(self, uploaded_file, destination_path):
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(uploaded_file.file.path, destination_path)

        if self._get_file_hash(uploaded_file.file.path) != self._get_file_hash(destination_path):
            raise exceptions.NotFound(self.INCORRECT_FILE_COPYING)

    def remove_objects(self, files):
        UploadedFile.objects.filter(uuid__in=[file.uuid for file in files]).delete()

    def remove_files(self, files):
        for file in files:
            os.remove(file)

    def get_destination_paths(self, model_class, model_field, source_instance):
        model_field_value = getattr(source_instance, model_field)
        relative_path = os.path.join(
            model_class._meta.get_field('file').upload_to,
            f'{str(source_instance.uuid)}.{model_field_value.name.split(".")[-1]}'
        )
        absolute_path = os.path.join(MEDIA_ROOT, relative_path)
        return absolute_path, relative_path
