from django.apps import apps
from django.db.models import Exists, OuterRef
from mptt.managers import TreeManager


class CategoryManager(TreeManager):
    """ Class representing category manager """
    def get_categories_with_products(self):
        """ Get categories with products.

        Returns:
            Categories with products.
        """
        SellerProduct = apps.get_model('seller_products', 'SellerProduct')

        return self.model.objects.prefetch_related(
            'recommended_for',
        ).filter(
            Exists(SellerProduct.objects.filter(
                categories__isnull=False,
                categories=OuterRef('id'),
            )),
        )

    def get_categories_with_recommended(self):
        """ Get categories with recommended.

        Returns:
            Categories with recommended.
        """
        SellerProduct = apps.get_model('seller_products', 'SellerProduct')

        return self.model.objects.prefetch_related(
            'recommended_for',
        )