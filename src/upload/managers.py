from datetime import datetime, timedelta

from django.db.models import Manager


class UploadedFileManager(Manager):

    def get_by_uuid_and_author(self, uuid, user_id):
        return self.model.objects.filter(uuid=uuid, created_by=user_id).first()

    def get_by_uuids_and_author(self, uuids, user_id):
        return self.model.objects.filter(uuids=uuids, created_by=user_id).first()

    def older_than(self, sec):
        return self.model.objects.filter(created_at__lt=(datetime.now() - timedelta(seconds=sec)))
