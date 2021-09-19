from django.db import models
from mptt.managers import TreeManager
from django.apps import apps
from django.db.models import Exists, OuterRef


class CategoryManager(TreeManager):

    def get_categories_with_products(self):
        SellerProduct = apps.get_model('seller_products', 'SellerProduct')

        return self.model.objects.prefetch_related(
            'recommended_for'
        ).filter(
            Exists(SellerProduct.objects.filter(
                categories__isnull=False,
                categories=OuterRef('id'),
            ))
        )
