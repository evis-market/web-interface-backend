from django.db import models

from categories.models import Category
from geo_regions.models import GeoRegion
from sellers.models import Seller


# from languages.models import Language
# from product_data_types.models import DateType, DataFormat
# from data_delivery_types.models import DataDeliveryType
# from data_samples.models import DataSamples


class DataSample(models.Model):
    name = models.CharField('Data Sample', max_length=100)
    descr = models.TextField('Description', blank=True, null=False, default='')
    path = models.FilePathField('Path to data sample', max_length=255)

    class Meta:
        db_table = 'data_samples'
        verbose_name = 'Data sample'
        verbose_name_plural = 'Data samples'

    def __str__(self):
        return f'{self.name} - {self.path}'


class DataUrl(models.Model):
    name = models.CharField('Data url', max_length=100)
    descr = models.TextField('Description', blank=True, null=False, default='')
    url = models.URLField('Path to data sample')

    # data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    # data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'data_urls'
        verbose_name = 'Data url'
        verbose_name_plural = 'Data urls'

    def __str__(self):
        return f'{self.name} - {self.url}'


class SellerProduct(models.Model):
    name = models.CharField('Product for sale', max_length=500)
    descr = models.TextField('Description', blank=True, null=False, default='')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    price_per_one_time = models.FloatField('Price per one time usage', blank=True, null=False, default=None)
    price_per_month = models.FloatField('Price per month', blank=True, null=False, default=None)
    price_per_year = models.FloatField('Price per year', blank=True, null=False, default=None)
    price_by_request = models.FloatField('Price by request', blank=True, null=False, default=None)
    price_per_usage = models.BooleanField('Price per usage True/False', blank=True, null=False, default=None)
    price_per_usage_descr = models.TextField('Purhcase method description', blank=True, null=False, default=None)
    rating = models.FloatField('Rating', blank=True, null=True, default=None)
    total_reviews_cnt = models.IntegerField('Total count of reviews')

    categories = models.ManyToManyField(Category, verbose_name='Content categories', related_name='seller_products', blank=True)
    geo_regions = models.ManyToManyField(GeoRegion, verbose_name='Content geo-regions', related_name='seller_products', blank=True)
    # languages = models.ManyToManyField(Language, verbose_name='Content languages', related_name='seller_products', blank=True)
    # data_types = models.ManyToManyField(DataType, verbose_name='Content data types', related_name='seller_products', blank=True)
    # data_format = models.ManyToManyField(DataFormat, verbose_name='Content data formats', related_name='seller_products', blank=True)
    # data_delivery_types = models.ManyToManyField(DataDeliveryType, verbose_name='Content data types', related_name='seller_products', blank=True)
    data_samples = models.ManyToManyField(DataSample, verbose_name='Content data samples', related_name='seller_products', blank=True)
    data_urls = models.ManyToManyField(DataUrl, verbose_name='Content data urls', related_name='seller_products', blank=True)
    version = models.IntegerField('Version', default=1)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True)

    class Meta:
        db_table = 'seller_products'
        verbose_name = 'Seller Product'
        verbose_name_plural = 'Seller Products'

    def __str__(self):
        return f'{self.name} (Seller={self.seller.name}) {self.descr[:100]}...'
