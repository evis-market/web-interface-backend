from django.db import models


class DataDeliveryTypeManager(models.Manager):
    """ Class representing data delivery type manager """
    def get_all(self):
        """ Get all data delivery types.

        Returns:
            All data delivery types.
        """
        return self.model.objects.all()
