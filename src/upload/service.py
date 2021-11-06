import hashlib
import os
import shutil
import uuid
from django.core.files.base import File

from app import exceptions
from upload.models import UploadedFile


class UploadService:
    BUFFER_SIZE = 1000
    NOTFOUND_UPLOADED_FILE_MSG = 'File does not exist or you do not have access permissions to it'
    INCORRECT_FILE_COPYING = 'File from source destination copied incorrectly'
    TMP_FILE_NOT_FOUND = 'File not found in temp directory'
    NO_FILE_SUBMITTED = 'No file was submitted'
    NOT_FILE = 'The submitted data was not a file. Check the encoding type on the form'
    UUID_INVALID = 'UUID is not valid'

    def check_file_uploaded(self, request):
        if 'file' not in request.data:
            raise exceptions.BadRequest(self.NO_FILE_SUBMITTED)

        if not issubclass(request.data['file'].__class__, File):
            raise exceptions.BadRequest(self.NOT_FILE)

    def uuid_valid(self, file_uuid):
        try:
            uuid.UUID(str(file_uuid))
        except ValueError:
            raise exceptions.BadRequest(self.UUID_INVALID)

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

    def copy_file(self, source_path, destination_path):
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy(source_path, destination_path)

        if self._get_file_hash(source_path) != self._get_file_hash(destination_path):
            raise exceptions.NotFound(self.INCORRECT_FILE_COPYING)

    def remove_objects(self, files):
        UploadedFile.objects.filter(uuid__in=[file.uuid for file in files]).delete()

    def remove_files(self, files):
        for file in files:  # noqa: VNE002
            os.remove(file)

    def get_destination_path(self, destination_model, source_model_field, source_instance, destination_file_name,
                             destination_file_field='file'):
        source_model_field_value = getattr(source_instance, source_model_field)
        return os.path.join(
            destination_model._meta.get_field(destination_file_field).upload_to,
            f'{destination_file_name}.{source_model_field_value.name.split(".")[-1]}'
        )
