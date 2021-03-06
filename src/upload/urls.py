from django.urls import path

from upload.views import UploadedFileView


urlpatterns = [
    path('', UploadedFileView.as_view(), name='GetFileUploaded'),
    path('<str:uuid>', UploadedFileView.as_view(), name='UploadFile')
]
