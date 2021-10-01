from django.contrib.contenttypes.models import ContentType
from django.db.models import Manager


class UploadedFileManager(Manager):

    def get_by_uuid_and_author(self, uuid, user_id):
        return self.model.objects.filter(uuid=uuid, created_by=user_id).first()

    def get_by_uuids_and_author(self, uuids, user_id):
        return self.model.objects.filter(uuids=uuids, created_by=user_id).first()

    def save(self):
        pass

    def delete_by_uuids_and_user(self, uuids, user_id):
        self.model.objects.filter(uuid__in=uuids, created_by=user_id)
