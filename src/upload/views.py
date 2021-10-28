from collections import OrderedDict

from django.db import transaction
from django.http import QueryDict
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from app.response import response_ok
from upload.serializers import UploadedFileSerializer, UploadedFileUpdateSerializer
from upload.service import UploadService


class UploadedFileView(GenericAPIView):
    """
    URL: `/api/v1/upload/:uuid`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
            "uploaded_file": {
                "file_url": "/media/uploaded_files_tmp/247ad31c927149ca940a13017f755fd9.pdf",
                "created_by": 1,
                "created_at": "2021-10-26T21:20:55.891438Z",
                "updated_at": "2021-10-26T21:20:55.891534Z",
                "file_name_original": "2_5330012327951470428.pdf"
            },
            "status": "OK"
        }

    Method: `POST`

    URL: `/api/v1/upload>/`
    Content-type: `multipart/form-data`

    **Request**
        {
            "file": "upload_file_here"
        }

    **Successful response**

        HTTP status Code: 200

        {
            "uuid": "1170a5f8-b9d3-4742-adda-eba3f4e08be6",
            "status": "OK"
        }

    """
    serializer_class = UploadedFileSerializer
    update_serializer_class = UploadedFileUpdateSerializer
    upload_service = UploadService()
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid, format=None):
        self.upload_service.uuid_valid(uuid)
        created_by = request.user.id
        uploaded_file = self.upload_service.get_object(uuid, created_by)
        serializer = self.serializer_class(uploaded_file)
        return response_ok({
            'uploaded_file': serializer.data
        })

    def post(self, request, format=None):
        self.upload_service.check_file_uploaded(request)
        data = OrderedDict({'created_by': request.user.id})
        data.update(request.data)
        serializer = self.update_serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            uploaded_file = self.upload_service.create_object(data=serializer.validated_data)
        return response_ok({'uuid': uploaded_file.uuid})
