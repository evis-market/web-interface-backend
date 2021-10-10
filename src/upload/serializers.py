from rest_framework import serializers

from upload.models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, instance):
        return instance.file.url

    class Meta:
        model = UploadedFile
        fields = [
            'file',
            'created_by',
            'file_url'
        ]
