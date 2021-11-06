import uuid as uuid
from django.db import models
from djmoney.models.fields import MoneyField

from sales.managers import SaleManager


class Sale(models.Model):
    created_at = models.DateTimeField('Created', auto_now_add=True)
    uuid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, primary_key=True)
    seller = models.ForeignKey('sellers.Seller', related_name='Seller', on_delete=models.CASCADE)
    buyer = models.ForeignKey('users.User', related_name='Buyer', on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=6)

    objects = SaleManager()

    class Meta:
        db_table = 'sales'
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ('created_at',)
        constraints = [
            models.CheckConstraint(
                name='buyer_not_seller',
                check=~models.Q(buyer=models.F('seller')),
            ),
        ]

    def __str__(self):
        return str(self.uuid)


class SaleProduct(models.Model):
    sale = models.ForeignKey('Sale', related_name='sale_product', on_delete=models.CASCADE)
    seller_product_archive = models.ForeignKey('seller_products.SellerProductArchive', related_name='sale_product',
                                               on_delete=models.CASCADE)

    objects = SaleManager()

    class Meta:
        db_table = 'sale_products'
        verbose_name = 'SaleProduct'
        verbose_name_plural = 'SaleProducts'
        ordering = ('sale_id',)

    def __str__(self):
        return self.sale
