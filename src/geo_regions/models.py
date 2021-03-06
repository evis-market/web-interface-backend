import mptt.models as mptt_models
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

from geo_regions.managers import GeoRegionManager


class GeoRegion(mptt_models.MPTTModel):
    name = models.CharField('Name', max_length=190, db_index=True)
    iso_code = models.CharField('ISO Code', max_length=3, unique=True, validators=[MinLengthValidator(2), MaxLengthValidator(3)])
    parent = mptt_models.TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    objects = GeoRegionManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'geo_regions'
        verbose_name = 'Geo region'
        verbose_name_plural = 'Geo regions'
