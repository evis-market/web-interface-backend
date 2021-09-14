from django.db import models

from categories.models import Category
from data_delivery_types.models import DataDeliveryType
from geo_regions.models import GeoRegion
# from languages.models import Language
from product_data_types.models import DataFormat, DataType
from seller_products.managers import (
    SellerProductArchiveManager, SellerProductBaseManager, SellerProductDataSampleArchiveManager, SellerProductDataSampleManager,
    SellerProductDataUrlArchiveManager, SellerProductDataUrlManager, SellerProductManager)
from sellers.models import Seller


class SellerProductBase(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=500)
    descr = models.TextField('Description', blank=True, default='')
    price_per_one_time = models.FloatField('Price per one time usage', blank=True, null=True, default=None)
    price_per_month = models.FloatField('Price per month', blank=True, null=True, default=None)
    price_per_year = models.FloatField('Price per year', blank=True, null=True, default=None)
    price_by_request = models.FloatField('Price by request', blank=True, null=True, default=None)
    price_per_usage = models.BooleanField('Price per usage True/False', blank=True, null=True, default=None)
    price_per_usage_descr = models.TextField('Purhcase method description', blank=True, null=True, default=None)
    rating = models.FloatField('Rating', blank=True, null=True, default=None)
    total_reviews_cnt = models.IntegerField('Total count of reviews', default=0)
    version = models.IntegerField('Version', default=1)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    objects = SellerProductBaseManager()

    class Meta:
        abstract = True
        verbose_name = 'Seller Product'
        verbose_name_plural = 'Seller Products'

    def __str__(self):
        return f'{self.name} (Seller={self.seller.name}) {self.descr[:100]}...'


class SellerProduct(SellerProductBase):
    categories = models.ManyToManyField(Category, verbose_name='Content categories', blank=True, db_table='seller_product_categories')
    geo_regions = models.ManyToManyField(GeoRegion, verbose_name='Content geo regions', blank=True, db_table='seller_product_geo_regions')
    # languages = models.ManyToManyField(Language, verbose_name='Content languages', blank=True)
    data_types = models.ManyToManyField(DataType, verbose_name='Content data types', blank=True, db_table='seller_product_data_types')
    data_formats = models.ManyToManyField(DataFormat, verbose_name='Content data formats', blank=True, db_table='seller_product_data_formats')
    data_delivery_types = models.ManyToManyField(
        DataDeliveryType, verbose_name='Content data types', blank=True, db_table='seller_product_data_delivery_types'
    )

    objects = SellerProductManager()

    class Meta:
        abstract = False
        db_table = 'seller_products'


class SellerProductArchive(SellerProductBase):
    id = models.BigAutoField(primary_key=True)
    seller_product_id = models.IntegerField()  # this field would be populated from id field of SellerProduct model
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, verbose_name='Content categories', blank=True, db_table='seller_product_categories_archive')
    geo_regions = models.ManyToManyField(GeoRegion, verbose_name='Content geo-regions', blank=True, db_table='seller_product_geo_regions_archive')
    # languages = models.ManyToManyField(Language, verbose_name='Content languages', blank=True)
    data_types = models.ManyToManyField(DataType, verbose_name='Content data types', blank=True, db_table='seller_product_data_types_archive')
    data_formats = models.ManyToManyField(DataFormat, verbose_name='Content data formats', blank=True, db_table='seller_product_data_formats_archive')
    data_delivery_types = models.ManyToManyField(
        DataDeliveryType, verbose_name='Content data types', blank=True, db_table='seller_product_data_delivery_types_archive'
    )
    is_deleted = models.BooleanField(default=False)

    objects = SellerProductArchiveManager()

    class Meta:
        abstract = False
        db_table = 'seller_products_archive'
        unique_together = ['id', 'version']


class SellerProductDataSample(models.Model):
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='data_samples')
    url = models.URLField('URL')
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)

    objects = SellerProductDataSampleManager()

    class Meta:
        db_table = 'seller_product_data_samples'
        verbose_name = 'Data sample'
        verbose_name_plural = 'Data samples'

    def __str__(self):
        return f'{self.seller_product.name} - {self.url}'


class SellerProductDataUrl(models.Model):
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='data_urls')
    url = models.URLField('URL')
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)

    objects = SellerProductDataUrlManager()

    class Meta:
        db_table = 'seller_product_data_urls'
        verbose_name = 'Data url'
        verbose_name_plural = 'Data urls'

    def __str__(self):
        return f'{self.seller_product.name} - {self.url}'


class SellerProductDataSampleArchive(models.Model):
    seller_product = models.ForeignKey(SellerProductArchive, on_delete=models.CASCADE, related_name='data_samples_archive')
    url = models.URLField('URL')
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)

    objects = SellerProductDataSampleArchiveManager()

    class Meta:
        db_table = 'seller_product_data_samples_archive'
        verbose_name = 'Data sample archive'
        verbose_name_plural = 'Data samples archive'

    def __str__(self):
        return f'{self.seller_product.name} - {self.url}'


class SellerProductDataUrlArchive(models.Model):
    seller_product = models.ForeignKey(SellerProductArchive, on_delete=models.CASCADE, related_name='data_urls_archive')
    url = models.URLField('URL')
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)

    objects = SellerProductDataUrlArchiveManager()

    class Meta:
        db_table = 'seller_product_data_urls_archive'
        verbose_name = 'Data url archive'
        verbose_name_plural = 'Data urls archive'

    def __str__(self):
        return f'{self.seller_product.name} - {self.url}'
