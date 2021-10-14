from django.db import models

from data_delivery_types.managers import DataDeliveryTypeManager


class DataDeliveryType(models.Model):
    """ Class representing data delivery type

    Attributes:
            name (django.db.models.fields.CharField): model name
            objects (src.categories.managers): data delivery type manager
    """
    name = models.CharField('Name', unique=True, blank=False, null=False, max_length=190)

    objects = DataDeliveryTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'data_delivery_types'
        verbose_name = 'Data Delivery Type'
        verbose_name_plural = 'Data Delivery Types'
        ordering = ('name',)
