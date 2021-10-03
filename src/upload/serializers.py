from rest_framework import serializers

from upload.models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile

        fields = [
            'file',
            'created_by'
        ]
