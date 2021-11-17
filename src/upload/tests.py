import pytest
from django.core.files import File
from django.urls import reverse
from mixer.backend.django import mixer

from upload.models import UploadedFile
from upload.views import UploadedFileView
from rest_framework.test import APIRequestFactory, force_authenticate

from users.models import User

pytestmark = pytest.mark.django_db


class TestUploadedFileView:

    def test_get(self):
        """
        Test: get upload file data
        """
        user = mixer.blend(User)
        uploaded_file = mixer.blend(
            UploadedFile,
            file=File(open('app/test-files/test-logo.png', 'rb')),  # noqa: SIM115
            file_name_original='test-logo',
            created_by=user)
        url = reverse('UploadFile', kwargs={'uuid': uploaded_file.uuid})
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = UploadedFileView.as_view()(request=request, uuid=uploaded_file.uuid)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'

        assert len(response.data['uploaded_file']) == 5
        fields = {
            "file_url": f"/media/{uploaded_file.file}",
            "created_by": uploaded_file.created_by.id,
            "file_name_original": uploaded_file.file_name_original,
        }
        for key, value in fields.items():
            assert response.data['uploaded_file'][key] == value
        assert 'created_at' in response.data['uploaded_file']
        assert 'updated_at' in response.data['uploaded_file']

    def test_post(self):
        """
        Test: upload file
        """
        user = mixer.blend(User)
        request_data = {
            "file": open('app/test-files/test-file-1.py', 'rb')
        }
        url = reverse('GetFileUploaded')
        request = APIRequestFactory().post(url, data=request_data, format='multipart')
        force_authenticate(request, user=user)
        response = UploadedFileView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        assert 'uuid' in response.data
        assert 'file_url' in response.data
        assert len(response.data) == 3
