import typing as tp

from django.db import models
from rest_framework.exceptions import NotFound

from app.utils import copy_instance


class SellerProductBaseManager(models.Manager):

    def get_products_by_seller_id(self, seller):
        return self.model.objects.filter(seller=seller)

    def get_product_by_seller_id(self, pk, seller):
        return self.model.objects.filter(pk=pk, seller=seller).first()


class SellerProductManager(SellerProductBaseManager):
    def create(
        self, seller: int, categories: tp.List[int], geo_regions: tp.List[int], data_types: tp.List[int],
        data_formats: tp.List[int], data_delivery_types: tp.List[int], **kwargs
    ):
        instance = super().create(seller=seller, **kwargs)
        instance.categories.add(*categories)
        instance.geo_regions.add(*geo_regions)
        instance.data_types.add(*data_types)
        instance.data_formats.add(*data_formats)
        instance.data_delivery_types.add(*data_delivery_types)
        instance.save()
        return instance

    def update(
        self, instance, categories: tp.List[int], geo_regions: tp.List[int], data_types: tp.List[int],
        data_formats: tp.List[int], data_delivery_types: tp.List[int], **kwargs
    ):
        for column, column_value in kwargs.items():
            setattr(instance, column, column_value)
        instance.version += 1
        instance.categories.clear()
        instance.categories.add(*categories)
        instance.geo_regions.clear()
        instance.geo_regions.add(*geo_regions)
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
