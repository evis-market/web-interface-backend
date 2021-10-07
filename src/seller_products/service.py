import typing

from app import exceptions
from seller_products.models import (
    SellerProduct, SellerProductArchive, SellerProductDataSample, SellerProductDataSampleArchive, SellerProductDataUrl, SellerProductDataUrlArchive)
from sellers.models import Seller
from upload.service import UploadService


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
        upload_service = UploadService()
        seller = data.pop('seller')
        categories = data.pop('data_categories_ids')
        geo_regions = data.pop('data_geo_regions_ids')
        languages = data.pop('data_langs_ids')
        data_types = data.pop('data_types_ids')
        data_formats = data.pop('data_formats_ids')
        data_delivery_types = data.pop('data_delivery_types_ids')
        data_samples_uploaded = data.pop('data_samples', None)
        data_urls = data.pop('data_urls', None)
        seller_product = SellerProduct.objects.create(
            seller, categories, geo_regions, languages, data_types, data_formats, data_delivery_types, **data,
        )
        seller_product_acrhive = SellerProductArchive.objects.create_instance_from_seller_product(seller_product)

        if data_samples_uploaded:
            for file in data_samples_uploaded:
                # upload seller_product_data_samples
                absolute_file_path, relative_file_path = upload_service.get_destination_paths(
                    SellerProductDataSample, 'file', file
                )
                upload_service.copy_file_from_tmp(file, absolute_file_path)
                sp = SellerProductDataSample(seller_product=seller_product, file=relative_file_path)
                sp.save()

                # upload seller_product_data_samples into archive
                absolute_file_path, relative_file_path = upload_service.get_destination_paths(
                    SellerProductDataSampleArchive, 'file', file
                )
                upload_service.copy_file_from_tmp(file, absolute_file_path)
                sp = SellerProductDataSampleArchive(seller_product=seller_product_acrhive, file=relative_file_path)
                sp.save()

        if data_urls:
            SellerProductDataUrl.objects.bulk_create([
                SellerProductDataUrl(seller_product=seller_product, **du) for du in data_urls
            ])
            SellerProductDataUrlArchive.objects.bulk_create([
                SellerProductDataUrlArchive(seller_product=seller_product_acrhive, **du) for du in data_urls
            ])

    def update_object(self, seller_product, data: typing.Dict):
        upload_service = UploadService()
        categories = data.pop('data_categories_ids')
        geo_regions = data.pop('data_geo_regions_ids')
        languages = data.pop('data_langs_ids')
        data_types = data.pop('data_types_ids')
        data_formats = data.pop('data_formats_ids')
        data_delivery_types = data.pop('data_delivery_types_ids')
        data_samples_uploaded = data.pop('data_samples', None)
        data_urls = data.pop('data_urls', None)

        seller_product = SellerProduct.objects.update(
            seller_product, categories, geo_regions, languages, data_types, data_formats, data_delivery_types, **data,
        )
        seller_product_acrhive = SellerProductArchive.objects.create_instance_from_seller_product(seller_product)

        SellerProductDataSample.objects.delete_by_seller_product(seller_product=seller_product)
        SellerProductDataUrl.objects.delete_by_seller_product(seller_product=seller_product)

        if data_samples_uploaded:
            for file in data_samples_uploaded:
                # upload seller_product_data_samples
                absolute_file_path, relative_file_path = upload_service.get_destination_paths(
                    SellerProductDataSample, 'file', file
                )
                upload_service.copy_file_from_tmp(file, absolute_file_path)
                sp = SellerProductDataSample(seller_product=seller_product, file=relative_file_path)
                sp.save()

                # upload seller_product_data_samples into archive
                absolute_file_path, relative_file_path = upload_service.get_destination_paths(
                    SellerProductDataSampleArchive, 'file', file
                )
                upload_service.copy_file_from_tmp(file, absolute_file_path)
                sp = SellerProductDataSampleArchive(seller_product=seller_product_acrhive, file=relative_file_path)
                sp.save()

        if data_urls:
            SellerProductDataUrl.objects.bulk_create([
                SellerProductDataUrl(seller_product=seller_product, **du) for du in data_urls
            ])
            SellerProductDataUrlArchive.objects.bulk_create([
                SellerProductDataUrlArchive(seller_product=seller_product_acrhive, **du) for du in data_urls
            ])

    def delete_object(self, seller_product):
        seller_product.delete()
