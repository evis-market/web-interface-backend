from django.db import models

from data_delivery_types.managers import DataDeliveryTypeManager


class DataDeliveryType(models.Model):
    name = models.CharField('Name', unique=True, blank=False, null=False, max_length=190)

    objects = DataDeliveryTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'data_delivery_types'
        verbose_name = 'Data Delivery Type'
        verbose_name_plural = 'Data Delivery Types'
        ordering = ('name',)
