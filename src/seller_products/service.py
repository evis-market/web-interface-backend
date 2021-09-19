import typing

from app import exceptions
from seller_products.models import (
    SellerProduct, SellerProductArchive, SellerProductDataSample, SellerProductDataSampleArchive, SellerProductDataUrl, SellerProductDataUrlArchive)
from sellers.models import Seller


class SellerProductService:
    FORBIDDEN_SELLER_ACCESS_MSG = 'The current user is not registered as a Seller'
    NOTFOUND_SELLER_MSG = 'SellerProduct not found'

    def get_seller(self, user_id: int):
        seller = Seller.objects.get_seller_by_user_id(user_id)
        if not seller:
            raise exceptions.NotFound(msg=self.FORBIDDEN_SELLER_ACCESS_MSG)
        return seller

    def get_seller_product(self, pk: int, user_id: int):
        seller_product = SellerProduct.objects.get_product_by_seller_id(pk, user_id)
        if not seller_product:
            raise exceptions.NotFound(self.NOTFOUND_SELLER_MSG)
        return seller_product

    def create_object(self, data: typing.Dict):
        seller = data.pop('seller')
        categories = data.pop('categories')
        geo_regions = data.pop('geo_regions')
        languages = data.pop('languages')
        data_types = data.pop('data_types')
        data_formats = data.pop('data_formats')
        data_delivery_types = data.pop('data_delivery_types')
        data_samples = data.pop('data_samples')
        data_urls = data.pop('data_urls')
        seller_product = SellerProduct.objects.create(
            seller, categories, geo_regions, languages, data_types, data_formats, data_delivery_types, **data
        )

        SellerProductDataSample.objects.bulk_create([
            SellerProductDataSample(seller_product=seller_product, **ds) for ds in data_samples
        ])
        SellerProductDataUrl.objects.bulk_create([
            SellerProductDataUrl(seller_product=seller_product, **du) for du in data_urls
        ])

        seller_product_acrhive = SellerProductArchive.objects.create_instance_from_seller_product(seller_product)
        SellerProductDataSampleArchive.objects.bulk_create([
            SellerProductDataSampleArchive(seller_product=seller_product_acrhive, **ds) for ds in data_samples
        ])
        SellerProductDataUrlArchive.objects.bulk_create([
            SellerProductDataUrlArchive(seller_product=seller_product_acrhive, **du) for du in data_urls
        ])

    def update_object(self, seller_product, data: typing.Dict):
        categories = data.pop('categories')
        geo_regions = data.pop('geo_regions')
        languages = data.pop('languages')
        data_types = data.pop('data_types')
        data_formats = data.pop('data_formats')
        data_delivery_types = data.pop('data_delivery_types')
        data_samples = data.pop('data_samples')
        data_urls = data.pop('data_urls')

        seller_product = SellerProduct.objects.update(
            seller_product, categories, geo_regions, languages, data_types, data_formats, data_delivery_types, **data
        )

        SellerProductDataSample.objects.delete_by_seller_product(seller_product=seller_product)
        SellerProductDataUrl.objects.delete_by_seller_product(seller_product=seller_product)
        SellerProductDataSample.objects.bulk_create([
            SellerProductDataSample(seller_product=seller_product, **ds) for ds in data_samples
        ])
        SellerProductDataUrl.objects.bulk_create([
            SellerProductDataUrl(seller_product=seller_product, **du) for du in data_urls
        ])

        seller_product_acrhive = SellerProductArchive.objects.create_instance_from_seller_product(seller_product)
        SellerProductDataSampleArchive.objects.bulk_create([
            SellerProductDataSampleArchive(seller_product=seller_product_acrhive, **ds) for ds in data_samples
        ])
        SellerProductDataUrlArchive.objects.bulk_create([
            SellerProductDataUrlArchive(seller_product=seller_product_acrhive, **du) for du in data_urls
        ])

    def delete_object(self, seller_product):
        seller_product.delete()
