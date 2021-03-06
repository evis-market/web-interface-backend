import os
from django.core.validators import MinValueValidator
from django.db import models

from categories.models import Category
from data_delivery_types.models import DataDeliveryType
from geo_regions.models import GeoRegion
from languages.models import Language
from product_data_types.models import DataFormat, DataType
from seller_products.managers import (
    SellerProductArchiveManager, SellerProductBaseManager, SellerProductDataSampleArchiveManager, SellerProductDataSampleManager,
    SellerProductDataUrlArchiveManager, SellerProductDataUrlManager, SellerProductManager)
from sellers.models import Seller


class SellerProductBase(models.Model):
    """ Class representing base seller product.

    Attributes:
          seller (django.db.models.fields.related.ForeignKey): seller
          name (django.db.models.fields.CharField): seller product name
          descr (django.db.models.fields.TextField): seller product description
          price_per_one_time (django.db.models.fields.FloatField): price per one time
          price_per_month (django.db.models.fields.FloatField): price per month
          price_per_year (django.db.models.fields.FloatField): price per year
          price_by_request (django.db.models.fields.BooleanField): price by request or not
          price_per_usage (django.db.models.fields.BooleanField): price per usage or not
          price_per_usage_descr (django.db.models.fields.TextField): price per usage description
          rating (django.db.models.fields.FloatField): rating
          total_reviews_cnt (django.db.models.fields.IntegerField): total reviews count
          version (django.db.models.fields.IntegerField): version
          created_at (django.db.models.fields.DateTimeField): created at date time
          updated_at (django.db.models.fields.DateTimeField): updated at date time
          objects (src.seller_products.managers): seller product base manager
    """
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=500)
    descr = models.TextField('Description', blank=True, default='')
    price_per_one_time = models.FloatField('Price per one time usage', blank=True, default=0,
                                           validators=[MinValueValidator(0.0)])
    price_per_month = models.FloatField('Price per month', blank=True, default=0, validators=[MinValueValidator(0.0)])
    price_per_year = models.FloatField('Price per year', blank=True, default=0, validators=[MinValueValidator(0.0)])
    price_by_request = models.BooleanField('Price by request True/False', blank=True, default=False)
    price_per_usage = models.BooleanField('Price per usage True/False', blank=True, default=False)
    price_per_usage_descr = models.TextField('Purchase method description', blank=True, default=0)
    rating = models.FloatField('Rating', blank=True, default=0, validators=[MinValueValidator(0.0)])
    total_reviews_cnt = models.IntegerField('Total count of reviews', default=0, validators=[MinValueValidator(0.0)])
    version = models.IntegerField('Version', default=1)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    objects = SellerProductBaseManager()

    class Meta:
        abstract = True
        verbose_name = 'Seller Product'
        verbose_name_plural = 'Seller Products'

    def __str__(self):
        return f'{self.name} {self.descr[:100]}...'


class SellerProductQuerySet(models.QuerySet):
    pass


class SellerProduct(SellerProductBase):
    """ Class representing seller products.

    Attributes:
          categories (django.db.models.fields.related.ManyToManyField): categories list
          geo_regions (django.db.models.fields.related.ManyToManyField): geo regions list
          languages (django.db.models.fields.related.ManyToManyField): languages list
          data_types (django.db.models.fields.related.ManyToManyField): data types list
          data_formats (django.db.models.fields.related.ManyToManyField): data formats list
          data_delivery_types (django.db.models.fields.related.ManyToManyField): data delivery types list
    """
    categories = models.ManyToManyField(Category, verbose_name='Content categories', blank=True,
                                        db_table='seller_product_categories')
    geo_regions = models.ManyToManyField(GeoRegion, verbose_name='Content geo regions', blank=True,
                                         db_table='seller_product_geo_regions')
    languages = models.ManyToManyField(Language, verbose_name='Content languages', blank=True,
                                       db_table='seller_product_languages')
    data_types = models.ManyToManyField(DataType, verbose_name='Content data types', blank=True,
                                        db_table='seller_product_data_types')
    data_formats = models.ManyToManyField(DataFormat, verbose_name='Content data formats', blank=True,
                                          db_table='seller_product_data_formats')
    data_delivery_types = models.ManyToManyField(
        DataDeliveryType, verbose_name='Content data types', blank=True, db_table='seller_product_data_delivery_types',
    )

    objects = SellerProductManager()

    class Meta:
        abstract = False
        db_table = 'seller_products'


class SellerProductArchive(SellerProductBase):
    """ Class representing seller product archive.

    Attributes:
          id (django.db.models.fields.BigAutoField): seller product archive id
          seller_product_id (django.db.models.fields.IntegerField): seller product id
          seller (django.db.models.fields.related.ForeignKey): seller
          categories (django.db.models.fields.related.ManyToManyField): categories list
          geo_regions (django.db.models.fields.related.ManyToManyField): geo regions list
          languages (django.db.models.fields.CharField): languages list
          data_types (django.db.models.fields.CharField): data types list
          data_formats (django.db.models.fields.CharField): data formats list
          data_delivery_types (django.db.models.fields.CharField): data delivery types list
          is_deleted (django.db.models.fields.BooleanField): seller product archive is deleted or not
          objects (src.seller_products.managers): seller product archive manager
    """
    id = models.BigAutoField(primary_key=True)
    seller_product_id = models.IntegerField()  # this field would be populated from id field of SellerProduct model
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, verbose_name='Content categories', blank=True,
                                        db_table='seller_product_categories_archive')
    geo_regions = models.ManyToManyField(GeoRegion, verbose_name='Content geo-regions', blank=True,
                                         db_table='seller_product_geo_regions_archive')
    languages = models.ManyToManyField(Language, verbose_name='Content languages', blank=True,
                                       db_table='seller_product_languages_archive')
    data_types = models.ManyToManyField(DataType, verbose_name='Content data types', blank=True,
                                        db_table='seller_product_data_types_archive')
    data_formats = models.ManyToManyField(DataFormat, verbose_name='Content data formats', blank=True,
                                          db_table='seller_product_data_formats_archive')
    data_delivery_types = models.ManyToManyField(
        DataDeliveryType, verbose_name='Content data types', blank=True,
        db_table='seller_product_data_delivery_types_archive',
    )
    is_deleted = models.BooleanField(default=False)

    objects = SellerProductArchiveManager()

    class Meta:
        abstract = False
        db_table = 'seller_products_archive'
        unique_together = ['seller_product_id', 'version']


class SellerProductDataSample(models.Model):
    """ Class representing seller product data sample.

    Attributes:
          id (django.db.models.fields.BigAutoField): seller product archive id
          seller_product_id (django.db.models.fields.IntegerField): seller product id
          seller (django.db.models.fields.related.ForeignKey): seller
          categories (django.db.models.fields.related.ManyToManyField): categories list
          geo_regions (django.db.models.fields.related.ManyToManyField): geo regions list
          languages (django.db.models.fields.CharField): languages list
          data_types (django.db.models.fields.CharField): data types list
          data_formats (django.db.models.fields.CharField): data formats list
          data_delivery_types (django.db.models.fields.CharField): data delivery types list
          is_deleted (django.db.models.fields.BooleanField): seller product archive is deleted or not
          objects (src.seller_products.managers): seller product archive manager
    """
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='data_samples')
    file = models.FileField(upload_to='seller_product_data_samples/')  # noqa: VNE002
    data_delivery_type = models.ForeignKey(DataDeliveryType, on_delete=models.CASCADE, blank=True, null=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE, blank=True, null=True)

    objects = SellerProductDataSampleManager()

    class Meta:
        db_table = 'seller_product_data_samples'
        verbose_name = 'Data sample'
        verbose_name_plural = 'Data samples'

    def __str__(self):
        return f'{self.seller_product.name} - {self.file}'

    @property
    def get_filename_without_extension(self):
        """ Get filename without extension

        Returns:
            Filename without extension.
        """
        return os.path.basename(self.file.name).split('.')[0]

    @property
    def get_filename_extension(self):
        """ Get filename extension

        Returns:
            Filename extension.
        """
        return os.path.basename(self.file.name).split('.')[-1]


class SellerProductDataUrl(models.Model):
    """ Class representing seller product data URL.

    Attributes:
          seller_product (django.db.models.fields.related.ForeignKey): seller product
          url (django.db.models.fields.URLField): seller product URL
          data_delivery_type (django.db.models.fields.related.ForeignKey): data delivery type
          data_format (django.db.models.fields.related.ForeignKey): data format
          objects (src.seller_products.managers): seller product data url manager
    """
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE, related_name='data_urls')
    url = models.URLField('URL')
    data_delivery_type = models.ForeignKey(DataDeliveryType, on_delete=models.CASCADE, blank=True, null=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE, blank=True, null=True)

    objects = SellerProductDataUrlManager()

    class Meta:
        db_table = 'seller_product_data_urls'
        verbose_name = 'Data url'
        verbose_name_plural = 'Data urls'

    def __str__(self):
        return f'{self.seller_product.name} - {self.url}'


class SellerProductDataSampleArchive(models.Model):
    """ Class representing seller product data sample archive.

    Attributes:
          seller_product (django.db.models.fields.related.ForeignKey): seller product
          file (django.db.models.fields.FileField): seller product data sample file
          data_delivery_type (django.db.models.fields.related.ForeignKey): data delivery type
          data_format (django.db.models.fields.related.ForeignKey): data format
          objects (src.seller_products.managers): seller product data sample archive manager
    """
    seller_product = models.ForeignKey(SellerProductArchive, on_delete=models.CASCADE,
                                       related_name='data_samples_archive')
    file = models.FileField(upload_to='seller_product_data_samples_archive/')  # noqa: VNE002
    data_delivery_type = models.ForeignKey(DataDeliveryType, on_delete=models.CASCADE, blank=True, null=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE, blank=True, null=True)

    objects = SellerProductDataSampleArchiveManager()

    class Meta:
        db_table = 'seller_product_data_samples_archive'
        verbose_name = 'Data sample archive'
        verbose_name_plural = 'Data samples archive'

    def __str__(self):
        return f'{self.seller_product.name} - {self.file}'


class SellerProductDataUrlArchive(models.Model):
    """ Class representing seller product data URL archive.

    Attributes:
          seller_product (django.db.models.fields.related.ForeignKey): seller product
          url (django.db.models.fields.URLField): seller product URL
          data_delivery_type (django.db.models.fields.related.ForeignKey): data delivery type
          data_format (django.db.models.fields.related.ForeignKey): data format
          objects (src.seller_products.managers): seller product data url archive manager
    """
    seller_product = models.ForeignKey(SellerProductArchive, on_delete=models.CASCADE, related_name='data_urls_archive')
    url = models.URLField('URL')
    data_delivery_type = models.ForeignKey(DataDeliveryType, on_delete=models.CASCADE, blank=True, null=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE, blank=True, null=True)

    objects = SellerProductDataUrlArchiveManager()

    class Meta:
        db_table = 'seller_product_data_urls_archive'
        verbose_name = 'Data url archive'
        verbose_name_plural = 'Data urls archive'

    def __str__(self):
        return f'{self.seller_product.name} - {self.url}'
