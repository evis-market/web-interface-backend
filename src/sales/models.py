import uuid as uuid
from django.db import models
from djmoney.models.fields import MoneyField
from sale.managers import SaleManager


class Sale(models.Model):
    created_at = models.DateTimeField('Created', auto_now_add=True)
    uuid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    seller_user_id = models.IntegerField()
    buyer_user_id = models.IntegerField()
    amount = MoneyField(max_digits=14, decimal_places=2)

    objects = SaleManager()

    class Meta:
        db_table = 'sales'
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ('created_at',)

    def __str__(self):
        return self.amount


class SaleProduct(models.Model):
    sale_id = models.ForeignKey('Sale', related_name='SaleProduct', on_delete=models.SET_NULL, null=True)
    seller_product_archive_id = models.ForeignKey('SellerProductArchive', related_name='SaleProduct', on_delete=models.SET_NULL, null=True)

    objects = SaleManager()

    class Meta:
        db_table = 'sale_product'
        verbose_name = 'SaleProduct'
        verbose_name_plural = 'SaleProducts'
        ordering = ('sale_id',)
