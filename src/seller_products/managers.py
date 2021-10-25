import typing as tp

from django.apps import apps
from django.db import models
from django.db.models import F, Value, Q
from django.db.models.functions import Reverse, Right, StrIndex, Substr

from app.utils import copy_instance


class SellerProductBaseManager(models.Manager):
    """ Class representing base seller products manager """

    def get_seller_product(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def get_products_by_seller_id(self, seller):
        return self.model.objects.select_related(
            'seller',
        ).prefetch_related(
            'categories',
            'geo_regions',
            'languages',
            'data_types',
            'data_formats',
            'data_delivery_types',
            'data_urls',
            'data_samples',
        ).filter(seller=seller)

    def get_product_by_seller_id(self, pk, seller):
        """ Get products by seller.

        Attributes:
                pk (str): private key
                seller (str): seller id

        Returns:
            Products by seller.
        """
        return self.model.objects.filter(pk=pk, seller=seller).first()

    def get_seller_product_detailed(self, pk):
        """ Get detailed info of seller product.

        Attributes:
                pk (str): private key

        Returns:
            Detailed info of seller product.
        """
        return self.model.objects.select_related(
            'seller',
        ).filter(pk=pk).first()

    def get_related_seller_products(self, pk):
        """ Get related seller products.

        Attributes:
                pk (str): private key

        Returns:
            Related seller products.
        """
        Category = apps.get_model('categories', 'Category')

        return self.model.objects.values(
            'id',
            'name',
            'descr',
            'price_per_one_time',
            'price_per_month',
            'price_per_year',
            'price_by_request',
            'price_per_usage',
            'price_per_usage_descr',
            'rating',
        ).filter(
            categories__id__in=Category.objects.get_queryset_descendants(
                Category.objects.filter(sellerproduct__id=pk),
                include_self=True,
            ),
        ).distinct()

    def get_seller_products_by_categories_and_name(self, name, categories):
        """ Get seller products by categories and name.

        Attributes:
                name (str): product name
                categories (list): categories list

        Returns:
            Seller products by categories and name.
        """
        Category = apps.get_model('categories', 'Category')

        query_filter = Q()
        if name:
            query_filter = Q(name__icontains=name)
        if categories:
            query_filter &= Q(categories__id__in=Category.objects.get_queryset_descendants(
                Category.objects.filter(id__in=categories),
                include_self=True,
            ))

        return self.model.objects.values(
            'id',
            'name',
            'price_per_one_time',
            'price_per_month',
            'price_per_year',
            'price_by_request',
            'price_per_usage',
            'price_per_usage_descr',
            'rating',
        ).filter(
            query_filter
        ).distinct()


class SellerProductManager(SellerProductBaseManager):
    """ Class representing seller products manager """

    def create(
        self, seller: int, categories: tp.List[int], geo_regions: tp.List[int], languages: tp.List[int],
        data_types: tp.List[int], data_formats: tp.List[int], data_delivery_types: tp.List[int], **kwargs
    ):
        """ Create seller product manager.

        Attributes:
                seller (int): seller id
                categories (list): categories list
                geo_regions (list): geo regions list
                languages (list): languages list
                data_types (list): data types list
                data_formats (list): data formats list
                data_delivery_types (list): data delivery types list

        Returns:
            Seller product manager instance.
        """
        instance = super().create(seller=seller, **kwargs)
        instance.categories.add(*categories)
        instance.geo_regions.add(*geo_regions)
        instance.languages.add(*languages)
        instance.data_types.add(*data_types)
        instance.data_formats.add(*data_formats)
        instance.data_delivery_types.add(*data_delivery_types)
        instance.save()
        return instance

    def update(
        self, instance, categories: tp.List[int], geo_regions: tp.List[int], languages: tp.List[int],
        data_types: tp.List[int], data_formats: tp.List[int], data_delivery_types: tp.List[int], **kwargs
    ):
        """ Update seller product manager.

        Attributes:
                instance (models.Manager): seller product manager instance
                categories (list): categories list
                geo_regions (list): geo regions list
                languages (list): languages list
                data_types (list): data types list
                data_formats (list): data formats list
                data_delivery_types (list): data delivery types list

        Returns:
            Seller product manager instance.
        """
        for column, column_value in kwargs.items():
            setattr(instance, column, column_value)
        instance.version += 1
        instance.categories.clear()
        instance.categories.add(*categories)
        instance.geo_regions.clear()
        instance.geo_regions.add(*geo_regions)
        instance.languages.clear()
        instance.languages.add(*languages)
        instance.data_types.clear()
        instance.data_types.add(*data_types)
        instance.data_formats.clear()
        instance.data_formats.add(*data_formats)
        instance.data_delivery_types.clear()
        instance.data_delivery_types.add(*data_delivery_types)
        instance.save()
        return instance


class SellerProductArchiveManager(SellerProductBaseManager):
    """ Class representing seller products archive manager """

    def create_instance_from_seller_product(self, seller_product):
        """ Create seller product manager.

        Attributes:
                seller_product (src.seller_products.models.SellerProduct): seller product

        Returns:
            Seller product archive manager instance.
        """
        instance = self.model()
        instance.seller_product_id = seller_product.id
        instance = copy_instance(seller_product, instance, exclude_fields=['id'])
        instance.save()
        return instance


class SellerProductDataSampleManager(models.Manager):
    """ Class representing seller products data sample manager """

    def get_by_seller_product(self, seller_product):
        """ Get seller products data sample by seller product.

        Attributes:
                seller_product (src.seller_products.models.SellerProduct): seller product

        Returns:
            Seller products data sample by seller product.
        """
        return self.model.objects.filter(seller_product=seller_product)

    def delete_by_seller_product_except_excluded_files(self, seller_product, filename_uuids_without_extension):
        """ Delete by seller product except excluded.

        Attributes:
               seller_product (src.seller_products.models.SellerProduct): seller product
               filename_uuids_without_extension (list): filenames list

        """
        objects = self.model.objects.annotate(
            last_slash_pos=StrIndex(Reverse('file'), Value('/')),
            filename=Right('file', F('last_slash_pos') - 1),
            dot_extension_pos=StrIndex('filename', Value('.')),
            filename_without_extension=Substr('filename', 1, F('dot_extension_pos') - 1)
        ).filter(
            seller_product=seller_product
        ).exclude(
            filename_without_extension__in=filename_uuids_without_extension
        )
        objects.delete()

    def file_exists(self, uuid):
        """ Check file exists.

        Attributes:
                uuid (models.UUIDField): file uuid

        Returns:
            True if file exists of False if not.
        """
        return self.model.objects.annotate(
            last_slash_pos=StrIndex(Reverse('file'), Value('/')),
            filename=Right('file', F('last_slash_pos') - 1),
            dot_extension_pos=StrIndex('filename', Value('.')),
            filename_without_extension=Substr('filename', 1, F('dot_extension_pos') - 1)
        ).filter(
            filename_without_extension=uuid
        ).first()


class SellerProductDataUrlManager(models.Manager):
    """ Class representing seller products data url manager """

    def get_by_seller_product(self, seller_product):
        """ Get product data url by seller product.

        Attributes:
                seller_product (src.seller_products.models.SellerProduct): seller product

        Returns:
            Product data url by seller product.
        """
        return self.model.objects.filter(seller_product=seller_product)

    def delete_by_seller_product(self, seller_product):
        """ Delete by seller product.

        Attributes:
               seller_product (src.seller_products.models.SellerProduct): seller product

        """
        self.model.objects.filter(seller_product=seller_product).delete()


class SellerProductDataSampleArchiveManager(models.Manager):
    pass


class SellerProductDataUrlArchiveManager(models.Manager):
    pass
