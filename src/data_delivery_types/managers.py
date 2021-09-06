from django.db import models


class DataDeliveryTypeManager(models.Manager):

    def get_all(self):
        return self.model.objects.all()
