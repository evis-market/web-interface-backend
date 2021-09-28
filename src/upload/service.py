import os
from hashlib import sha256

from django.core.exceptions import ObjectDoesNotExist
from app import exceptions

from upload.models import UploadedFile


class UploadedFileService:
    NOTFOUND_UPLOADED_FILE_MSG = 'File with = %s does not exist'
    NOTFOUND_MODEL = 'Model does not exist'
    NOTFOUND_MODEL_FIELD = 'Field does not exist'

    def create_object(self, data):
        try:
            model_class = UploadedFile.objects.get_model_class_by_name(data['model'])
        except ObjectDoesNotExist:
            raise exceptions.NotFound(msg=self.NOTFOUND_MODEL)

        if data['model_field'] not in model_class._meta.fields:
            raise exceptions.NotFound(msg=self.NOTFOUND_MODEL_FIELD)

        UploadedFile.objects.create(**data)

    def migrate_file(self, uuid):
        uploaded_file = UploadedFile.objects.get_by_uuid(uuid)
        if not uploaded_file:
            raise exceptions.NotFound(self.NOTFOUND_UPLOADED_FILE_MSG % uuid)

        source_file_hash = sha256(uploaded_file.file_path)

        destination_path = self.get_destination_path(uploaded_file)


    def get_destination_path(self, uploaded_file):
        model_class = UploadedFile.objects.get_model_class_by_uuid(uploaded_file.uuid)
        return model_class._meta.fields[uploaded_file.model_field].uploaded_to
