from django.contrib.contenttypes.models import ContentType
from django.db.models import Manager


class UploadedFileManager(Manager):

    def get_by_uuid(self, uuid):
        self.model.objects.filter(uuid=uuid).first()

    def get_model_class_by_uuid(self, uuid):
        content_type = ContentType.objects.get(model=uuid.model.lower())
        return content_type.model_class()

    def get_model_class_by_name(self, model_name):
        content_type = ContentType.objects.get(model=model_name.lower())
        return content_type.model_class()

    def save(self):
        pass
