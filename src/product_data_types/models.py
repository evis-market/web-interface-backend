from django.db import models

from product_data_types.managers import DataFormatManager, DataTypeManager


class DataType(models.Model):
    """ Class representing data type

    Attributes:
            name (django.db.models.fields.CharField): model name
            objects (src.categories.managers): data type manager
    """
    name = models.CharField('Name', unique=True, blank=False, null=False, max_length=190)

    objects = DataTypeManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'data_types'
        verbose_name = 'Data Type'
        verbose_name_plural = 'Data Types'
        ordering = ('name',)


class DataFormat(models.Model):
    """ Class representing data format

    Attributes:
            data_type_id (django.db.models.fields.related.ForeignKey): data type id
            name (django.db.models.fields.CharField): model name
            objects (src.categories.managers): data format manager
    """
    data_type_id = models.ForeignKey('DataType', related_name='DataFormat', on_delete=models.SET_NULL, null=True)
    name = models.CharField('Name', unique=True, blank=False, null=False, max_length=190)

    objects = DataFormatManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'data_format'
        verbose_name = 'Data Format'
        verbose_name_plural = 'Data Formats'
        ordering = ('name',)
