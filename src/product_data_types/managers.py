from django.db import models


class DataTypeManager(models.Manager):
    """ Class representing data type manager """
    def get_all(self):
        return self.model.objects.all()


class DataFormatManager(models.Manager):
    """ Class representing data format manager """
    def get_all(self):
        return self.model.objects.all()
