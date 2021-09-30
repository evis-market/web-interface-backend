import os
from hashlib import sha256

from django.core.exceptions import ObjectDoesNotExist
from app import exceptions

from upload.models import UploadedFile


class UploadService:
    NOTFOUND_UPLOADED_FILE_MSG = 'File does not exist or you do not have access permissions to it'

    def get_object(self, uuid, created_by):
        uploaded_file = UploadedFile.objects.filter(uuid=uuid, created_by=created_by)
        if not uploaded_file:
            raise exceptions.NotFound(msg=self.NOTFOUND_UPLOADED_FILE_MSG)
        return uploaded_file

    def create_object(self, data):
        return UploadedFile.objects.create(**data)

    def migrate_file(self, uuid, user_id):
        uploaded_file = UploadedFile.objects.get_by_uuid(uuid, user_id)
        if not uploaded_file:
            raise exceptions.NotFound(self.NOTFOUND_UPLOADED_FILE_MSG)

        source_file_hash = sha256(uploaded_file.file_path)

        destination_path = self.get_destination_path(uploaded_file)

    def get_destination_path(self, uploaded_file):
        model_class = UploadedFile.objects.get_model_class_by_uuid(uploaded_file.uuid)
        return model_class._meta.fields[uploaded_file.model_field].uploaded_to
