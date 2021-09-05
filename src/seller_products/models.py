from django.db import models

from categories.models import Category
from geo_regions.models import GeoRegion
from sellers.models import Seller


# from languages.models import Language
from product_data_types.models import DataType, DataFormat
# from data_delivery_types.models import DataDeliveryType
# from data_samples.models import DataSamples


class SellerProductBase(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField('Name', max_length=500)
    descr = models.TextField('Description', blank=True, null=False, default='')
    price_per_one_time = models.FloatField('Price per one time usage', blank=True, null=False, default=None)
    price_per_month = models.FloatField('Price per month', blank=True, null=False, default=None)
    price_per_year = models.FloatField('Price per year', blank=True, null=False, default=None)
    price_by_request = models.FloatField('Price by request', blank=True, null=False, default=None)
    price_per_usage = models.BooleanField('Price per usage True/False', blank=True, null=False, default=None)
    price_per_usage_descr = models.TextField('Purhcase method description', blank=True, null=False, default=None)
    rating = models.FloatField('Rating', blank=True, null=True, default=None)
    total_reviews_cnt = models.IntegerField('Total count of reviews')

    version = models.IntegerField('Version', default=1)
    created_at = models.DateTimeField('Created', auto_now_add=True)
    updated_at = models.DateTimeField('Updated', auto_now=True)

    class Meta:
        abstract = True
        verbose_name = 'Seller Product'
        verbose_name_plural = 'Seller Products'

    def __str__(self):
        return f'{self.name} (Seller={self.seller.name}) {self.descr[:100]}...'


class SellerProduct(SellerProductBase):
    categories = models.ManyToManyField(Category, verbose_name='Content categories', blank=True)
    geo_regions = models.ManyToManyField(GeoRegion, verbose_name='Content geo regions', blank=True)
    # languages = models.ManyToManyField(Language, verbose_name='Content languages', blank=True)
    data_types = models.ManyToManyField(DataType, verbose_name='Content data types', blank=True)
    data_format = models.ManyToManyField(DataFormat, verbose_name='Content data formats', blank=True)
    # data_delivery_types = models.ManyToManyField(DataDeliveryType, verbose_name='Content data types', blank=True)
    # data_samples = models.ManyToManyField(SellerProductDataSample, verbose_name='Content data samples', blank=True)
    # data_urls = models.ManyToManyField(SellerProductDataUrl, verbose_name='Content data urls', blank=True)

    class Meta:
        abstract = False
        db_table = 'seller_products'


class SellerProductArchive(SellerProductBase):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE,)
    # categories = models.ManyToManyField(Category, verbose_name='Content categories', blank=True)
    # geo_regions = models.ManyToManyField(GeoRegion, verbose_name='Content geo-regions', blank=True)
    # languages = models.ManyToManyField(Language, verbose_name='Content languages', blank=True)
    # data_types = models.ManyToManyField(DataType, verbose_name='Content data types', blank=True)
    # data_format = models.ManyToManyField(DataFormat, verbose_name='Content data formats', blank=True)
    # data_delivery_types = models.ManyToManyField(DataDeliveryType, verbose_name='Content data types', blank=True)
    # data_samples = models.ManyToManyField(DataSample, verbose_name='Content data samples', blank=True)
    # data_urls = models.ManyToManyField(DataUrl, verbose_name='Content data urls', blank=True)

    class Meta:
        abstract = False
        db_table = 'seller_products_archive'


class SellerProductDataSample(models.Model):
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE)
    url = models.URLField('URL')
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'seller_product_data_samples'
        verbose_name = 'Data sample'
        verbose_name_plural = 'Data samples'

    def __str__(self):
        return f'{self.name} - {self.path}'


class SellerProductDataUrl(models.Model):
    seller_product = models.ForeignKey(SellerProduct, on_delete=models.CASCADE)
    url = models.URLField('URL')
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE)
    data_format = models.ForeignKey(DataFormat, on_delete=models.CASCADE)

    class Meta:
        db_table = 'seller_product_data_urls'
        verbose_name = 'Data url'
        verbose_name_plural = 'Data urls'

    def __str__(self):
        return f'{self.name} - {self.url}'
