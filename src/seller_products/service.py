import typing

from sellers.models import Seller
from seller_products.models import SellerProduct, SellerProductDataSample, SellerProductDataUrl, SellerProductArchive
from app import exceptions


class SellerProductService:
    FORBIDDEN_SELLER_ACCESS_MSG = 'The current user is not registered as a Seller'
    NOTFOUND_SELLER_MSG = 'SellerProduct not found'

    def get_seller(self, user_id: int):
        seller = Seller.objects.get_seller_by_user_id(user_id)
        if not seller:
            raise exceptions.Forbidden(msg=self.FORBIDDEN_SELLER_ACCESS_MSG)
        return seller

    def get_seller_products(self, user_id: int):
        seller = self.get_seller(user_id)
        return SellerProduct.objects.get_products_by_seller_id(seller)

    def get_seller_product(self, pk: int, user_id: int):
        seller = self.get_seller(user_id)
        seller_product = SellerProduct.objects.get_product_by_seller_id(pk, seller)
        if not seller_product:
            raise exceptions.NotFound(self.NOTFOUND_SELLER_MSG)
        return seller_product

    def create_object(self, data: typing.Dict):
        seller = data.pop('seller')
        categories = data.pop('categories')
        geo_regions = data.pop('geo_regions')
        data_types = data.pop('data_types')
        data_formats = data.pop('data_formats')
        data_delivery_types = data.pop('data_delivery_types')
        data_samples = data.pop('data_samples')
        data_urls = data.pop('data_urls')
        seller_product = SellerProduct.objects.create(
            seller, categories, geo_regions, data_types, data_formats, data_delivery_types, **data
        )
        SellerProductDataSample.objects.bulk_create([
            SellerProductDataSample(seller_product=seller_product, **ds) for ds in data_samples
        ])
        SellerProductDataUrl.objects.bulk_create([
            SellerProductDataUrl(seller_product=seller_product, **du) for du in data_urls
        ])
        SellerProductArchive.objects.create_instance_from_seller_product(seller_product)

    def update_object(self, seller_product, data: typing.Dict):
        categories = data.pop('categories')
        geo_regions = data.pop('geo_regions')
        data_types = data.pop('data_types')
        data_formats = data.pop('data_formats')
        data_delivery_types = data.pop('data_delivery_types')
        data_samples = data.pop('data_samples')
        data_urls = data.pop('data_urls')

        seller_product = SellerProduct.objects.update(
            seller_product, categories, geo_regions, data_types, data_formats, data_delivery_types, **data
        )
        SellerProductDataSample.objects.filter(seller_product=seller_product).delete()
        SellerProductDataUrl.objects.filter(seller_product=seller_product).delete()
        SellerProductDataSample.objects.bulk_create([
            SellerProductDataSample(seller_product=seller_product, **ds) for ds in data_samples
        ])
        SellerProductDataUrl.objects.bulk_create([
            SellerProductDataUrl(seller_product=seller_product, **du) for du in data_urls
        ])
        SellerProductArchive.objects.create_instance_from_seller_product(seller_product)
        SellerProductArchive.objects.create_instance_from_seller_product(seller_product)

    def delete_object(self, seller_product):
        seller_product.delete()
