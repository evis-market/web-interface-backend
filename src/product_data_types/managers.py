from django.db import models


class DataTypeManager(models.Manager):
    def get_all(self):
        return self.model.objects.all()


class DataFormatManager(models.Manager):
    def get_all(self):
        return self.model.objects.all()
