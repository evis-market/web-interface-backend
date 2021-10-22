import logging
import os

from django.core.management.base import BaseCommand

from app.conf.base import MEDIA_ROOT
from seller_products.models import SellerProductDataSample
from upload.models import UploadedFile
from upload.service import UploadService


class Command(BaseCommand):
    help = """Remove files uploaded into temp directory and had not been moved to any other directory for a period of
    time specified in seconds as command line argument"""

    # Folders of model fields that would be cleared
    MODEL_FIELDS_TO_CLEAR = [
        {'model_class': SellerProductDataSample, 'model_field': 'file'},
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            '--time_in_seconds',
            help='',
            default=24 * 60 * 60,
            type=int
        )

    def handle(self, *args, **options):
        logging.info('Cleaning tmp upload folder... Started')
        upload_service = UploadService()
        temp_files = UploadedFile.objects.older_than(int(options['time_in_seconds']))
        upload_service.remove_files(os.path.join(MEDIA_ROOT, f) for f in temp_files.values_list('file', flat=True))
        upload_service.remove_objects(temp_files)
        logging.info('Cleaning tmp upload folder... Finished')
