import logging
import os
import time
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from app.conf.base import MEDIA_ROOT
from seller_products.models import SellerProductDataSample


class Command(BaseCommand):
    help = 'Remove files loaded into folders specified in model fields defined in class attribute MODEL_FIELDS_TO_CLEAR' \
           'But not bounded to model fields for a period of time presented as an command line argument: time_in_seconds' \
           'For the moment class attribute MODEL_FIELDS_TO_CLEAR is hardcoded' \
           'It does make sense to set it up as command line argument'

    # Folders of model fields that would be cleared
    MODEL_FIELDS_TO_CLEAR = [
        {'model_class': SellerProductDataSample, 'model_field': SellerProductDataSample._meta.get_field('file')}
    ]

    class ModelFieldCleaner:
        def __init__(self, model_class, model_field, datetime_unix_from):
            self.model_class = model_class
            self.model_field = model_field
            self.datetime_unix_from = datetime_unix_from

        def __call__(self, *args, **kwargs):
            self.remove_unbounded_files()

        def remove_unbounded_files(self):
            logging.info(
                'Remove_unbounded_files started, files created before %s will be removed',
                datetime.utcfromtimestamp(self.datetime_unix_from).strftime('%Y-%m-%d %H:%M:%S')
            )
            upload_path = self.model_field.upload_to
            absolute_path = os.path.join(MEDIA_ROOT, upload_path)
            files_in_catalog = set(os.path.join(upload_path, f) for f in os.listdir(absolute_path))
            model_files = set(self.model_class.objects.all().values_list(self.model_field.name, flat=True))

            for file in files_in_catalog.difference(model_files):  # noqa: VNE002
                filepath = os.path.join(MEDIA_ROOT, file)
                if os.path.getmtime(filepath) < self.datetime_unix_from:
                    logging.info('File =', filepath, ' removed..')
                    os.remove(filepath)
            logging.info('Remove_unbounded_files finished')

    def add_arguments(self, parser):
        parser.add_argument(
            '-t',
            '--time_in_seconds',
            help='',
            default=24 * 60 * 60,
            type=int
        )

    @staticmethod
    def _get_from_unixtime(current_datetime, time_in_seconds):
        from_datetime = current_datetime - timedelta(seconds=time_in_seconds)
        return time.mktime(from_datetime.timetuple())

    def handle(self, *args, **options):
        logging.info('Removing unbounded files... Started')
        current_datetime = datetime.now()
        datetime_unix_from = self._get_from_unixtime(current_datetime, int(options['time_in_seconds']))
        for model_field_dict in self.MODEL_FIELDS_TO_CLEAR:
            model_field_cleaner = self.ModelFieldCleaner(**model_field_dict, datetime_unix_from=datetime_unix_from)
            logging.info(
                'Removing files started for model = %s; field = %s;',
                (model_field_cleaner.model_class, model_field_cleaner.model_field)
            )
            model_field_cleaner()
        logging.info('Removing unbounded files... Finished')
