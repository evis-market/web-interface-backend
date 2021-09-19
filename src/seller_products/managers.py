import typing as tp

from django.apps import apps
from django.db import models

from app.utils import copy_instance


class SellerProductBaseManager(models.Manager):

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
        return self.model.objects.filter(pk=pk, seller=seller).first()

    def get_seller_product_detailed(self, pk):
        return self.model.objects.select_related(
            'seller',
        ).filter(pk=pk).first()

    def get_related_seller_products(self, pk):
        Category = apps.get_model('categories', 'Category')

        return self.model.objects.values('id').filter(
            categories__id__in=Category.objects.get_queryset_descendants(
                Category.objects.filter(sellerproduct__id=pk),
                include_self=True,
            ),
        ).distinct()

    def get_seller_products_by_categories(self, categories):
        Category = apps.get_model('categories', 'Category')

        return self.model.objects.values('id').filter(
            categories__id__in=Category.objects.get_queryset_descendants(
                Category.objects.filter(id__in=categories),
                include_self=True,
            ),
        ).distinct()


class SellerProductManager(SellerProductBaseManager):
    def create(
        self, seller: int, categories: tp.List[int], geo_regions: tp.List[int], languages: tp.List[int],
        data_types: tp.List[int], data_formats: tp.List[int], data_delivery_types: tp.List[int], **kwargs
    ):
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
    def create_instance_from_seller_product(self, seller_product):
        instance = self.model()
        instance.seller_product_id = seller_product.id
        instance = copy_instance(seller_product, instance, exclude_fields=['id'])
        instance.save()
        return instance


class SellerProductDataSampleManager(models.Manager):

    def get_by_seller_product(self, seller_product):
        return self.model.objects.filter(seller_product=seller_product)

    def delete_by_seller_product(self, seller_product):
        self.model.objects.filter(seller_product=seller_product).delete()


class SellerProductDataUrlManager(models.Manager):
    def get_by_seller_product(self, seller_product):
        return self.model.objects.filter(seller_product=seller_product)

    def delete_by_seller_product(self, seller_product):
        self.model.objects.filter(seller_product=seller_product).delete()


class SellerProductDataSampleArchiveManager(models.Manager):
    pass


class SellerProductDataUrlArchiveManager(models.Manager):
    pass
