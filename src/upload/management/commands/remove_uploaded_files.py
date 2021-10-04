import os
import time
from datetime import datetime, timedelta

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


        print('Cleaning tmp upload folder... Finished')

    def remove_unbounded_files(self, older_than: int, model_class, model_field):
        # all files not bounded to models would be deleted
        # if their last modified time would be sooner than the following calculated
        from_datetime = datetime.now() - timedelta(older_than)
        from_datetime_unix = time.mktime(from_datetime.timetuple())

        upload_to_path = model_class._meta.get_field(model_field).upload_to
        absolute_path = os.path.join(MEDIA_ROOT, upload_to_path)
        files_in_catalog = set(os.path.join(upload_to_path, f) for f in os.listdir(absolute_path))
        seller_products_files = set(model_class.objects.all().values_list('file', flat=True))

        for file in files_in_catalog.difference(seller_products_files):
            filepath = os.path.join(MEDIA_ROOT, file)
            if os.path.getmtime(filepath) < from_datetime_unix:
                print(os.path.getmtime(filepath))
                print(from_datetime_unix)
                # os.remove(filepath)