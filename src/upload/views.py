from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from app.response import response_ok
from upload.serializers import UploadedFileSerializer
from upload.service import UploadService


class UploadedFileView(GenericAPIView):
    """
    URL: `/api/v1/upload/:uuid>`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
            "uploaded_file": {
                "file": "/media/uploaded_files_tmp/b2da7db5bb8546549afd529fe9f3c8c3.pdf",
                "created_by": 1
            },
            "status": "OK"
        }

    Method: `POST`

    URL: `/api/v1/upload>`

    **Successful response**

        HTTP status Code: 200

        {
            "status": "OK"
        }

    """
    serializer_class = UploadedFileSerializer
    upload_service = UploadService()
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid, format=None):
        created_by = request.user.id
        uploaded_file = self.upload_service.get_object(uuid, created_by)
        serializer = self.serializer_class(uploaded_file)
        return response_ok({
            'uploaded_file': serializer.data
        })

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        request.data['created_by'] = request.user.id
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            uploaded_file = self.upload_service.create_object(data=serializer.validated_data)
        return response_ok({'uuid': uploaded_file.uuid})
