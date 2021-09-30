from django.contrib.contenttypes.models import ContentType
from django.db.models import Manager


class UploadedFileManager(Manager):

    def get_by_uuid_and_author(self, uuid, user_id):
        self.model.objects.filter(uuid=uuid, created_by=user_id).first()

    def save(self):
        pass
