import uuid as uuid
from django.db import models
from djmoney.models.fields import MoneyField
from sales.managers import SaleManager


class Sale(models.Model):
    created_at = models.DateTimeField('Created', auto_now_add=True)
    uuid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4)
    seller = models.OneToOneField('sellers.Seller', related_name='Seller', on_delete=models.CASCADE)
    buyer = models.OneToOneField('users.User', related_name='Buyer', on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=6)

    objects = SaleManager()

    class Meta:
        db_table = 'sales'
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ('created_at',)

    def __str__(self):
        return self.amount


class SaleProduct(models.Model):
    sale = models.ForeignKey('Sale', related_name='SaleProduct', on_delete=models.CASCADE)
    seller_product_archive_id = models.ForeignKey('seller_products.SellerProductArchive', related_name='SaleProduct', on_delete=models.CASCADE)

    objects = SaleManager()

    class Meta:
        db_table = 'sale_products'
        verbose_name = 'SaleProduct'
        verbose_name_plural = 'SaleProducts'
        ordering = ('sale_id',)
