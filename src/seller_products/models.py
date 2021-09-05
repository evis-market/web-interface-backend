from django.db import models

from categories.models import Category
from sellers.models import Seller


class SellerProduct(models.Model):
    name = models.CharField('Product for sale', max_length=500)
    descr = models.TextField('Description', blank=True, null=False, default='')
    seller_id = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    price_per_one_time = models.FloatField('Price per one time usage', blank=True, null=False, default=None)
    price_per_month = models.FloatField('Price per month', blank=True, null=False, default=None)
    price_per_year = models.FloatField('Price per year', blank=True, null=False, default=None)
    price_by_request = models.FloatField('Price by request', blank=True, null=False, default=None)
    price_per_usage = models.BooleanField('Price per usage True/False', blank=True, null=False, default=None)
    price_per_usage_descr = models.TextField('Purhcase method description', blank=True, null=False, default=None)
    rating = models.FloatField('Rating', blank=True, null=True, default=None)
    total_reviews_cnt = models.IntegerField('Total count of reviews')
    version = models.IntegerField('Version', default=1)

    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True)




