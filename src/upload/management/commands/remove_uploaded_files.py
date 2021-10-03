import os
from django.core.management.base import BaseCommand

from upload.models import UploadedFile
from upload.service import UploadService
from seller_products.models import SellerProductDataSample
from app.conf.base import MEDIA_ROOT


class Command(BaseCommand):
    help = 'Remove files uploaded into temp directory and had not been moved to ' \
           'any other directory for a period of time'

    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            '--time_in_seconds',
            help='',
            default=24 * 60 * 60,
            type=int
        )

    def handle(self, *args, **options):
        print('Cleaning tmp upload folder... Started')
        upload_service = UploadService()
        temp_files = UploadedFile.objects.older_than(int(options['time_in_seconds']))
        upload_service.remove_files(os.path.join(MEDIA_ROOT, f) for f in temp_files)
        upload_service.remove_objects(temp_files)
        # data_samples = SellerProductDataSample.objects.all()
        # for ds in data_samples:
        #
        print('Cleaning tmp upload folder... Finished')
