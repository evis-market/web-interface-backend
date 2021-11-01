import os

import typing

from app import exceptions
from app.conf.base import MEDIA_ROOT
from seller_products.models import (
    SellerProduct, SellerProductArchive, SellerProductDataSample, SellerProductDataSampleArchive, SellerProductDataUrl,
    SellerProductDataUrlArchive)
from sellers.models import Seller
from upload.service import UploadService


class SellerProductService:
    """ Seller product service """
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
        """ Creates object.

            Args:
                data (dict): params dict

            Attributes:
                upload_service (src.upload.service.UploadService): upload service
                seller (str): seller
                categories (list): categories list
                geo_regions (list): geo regions list
                languages (list): languages list
                data_types (list): data types list
                data_formats (list): data formats list
                data_delivery_types (list): data delivery types list
                data_samples_uploaded (list): data samples uploaded list
                data_urls (list): data urls list
                seller_product (src.seller_products.models.SellerProduct): seller product
                seller_product_acrhive (src.seller_products.models.SellerProductArchive): seller product archive

        """
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

        self._create_data_samples(data_samples_uploaded, upload_service, seller_product, seller_product_acrhive)
        self._create_data_urls(data_urls, seller_product, seller_product_acrhive)

    def _create_data_samples(self, data_samples_uploaded, upload_service, seller_product, seller_product_acrhive):
        if data_samples_uploaded:
            for data_sample in data_samples_uploaded:
                # upload seller_product_data_samples
                upload_to = upload_service.get_destination_path(SellerProductDataSample, 'file', data_sample,
                                                                data_sample.uuid)
                upload_service.copy_file_from_tmp(data_sample, os.path.join(MEDIA_ROOT, upload_to))
                sp = SellerProductDataSample(seller_product=seller_product, file=upload_to)
                sp.save()

                # upload seller_product_data_samples into archive
                upload_to = upload_service.get_destination_path(SellerProductDataSampleArchive, 'file', data_sample,
                                                                data_sample.uuid)
                upload_service.copy_file_from_tmp(data_sample, os.path.join(MEDIA_ROOT, upload_to))
                sp = SellerProductDataSampleArchive(seller_product=seller_product_acrhive, file=upload_to)
                sp.save()

    def _create_data_urls(self, data_urls, seller_product, seller_product_acrhive):
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

        self._update_data_samples(data_samples_uploaded, upload_service, seller_product, seller_product_acrhive)
        self._update_data_urls(data_urls, seller_product, seller_product_acrhive)

    def _update_data_samples(self, data_samples_uploaded, upload_service, seller_product, seller_product_acrhive):
        # todo: check if no files supplied - delete all SellerProductDataSample or not ?
        if data_samples_uploaded:
            # first, lets delete those files that are not longer presented as data_samples in updated seller_product
            SellerProductDataSample.objects.delete_by_seller_product_except_excluded_files(
                seller_product,
                [data_sample.uuid for data_sample in data_samples_uploaded]
            )

            # then upload new files into respective directories and updated its data in seller_product models
            for file in data_samples_uploaded:  # noqa: VNE002
                if not SellerProductDataSample.objects.file_exists(file.uuid):
                    upload_to = upload_service.get_destination_path(SellerProductDataSample, 'file', file, file.uuid)
                    upload_service.copy_file_from_tmp(file, os.path.join(MEDIA_ROOT, upload_to))
                    sp = SellerProductDataSample(seller_product=seller_product, file=upload_to)
                    sp.save()

            # copying files loaded on previous step into archive, updating seller_product archive model instances
            for data_sample in SellerProductDataSample.objects.filter(seller_product=seller_product):
                upload_to = upload_service.get_destination_path(SellerProductDataSampleArchive, 'file', data_sample,
                                                                data_sample.get_filename_without_extension)
                source_file_path = os.path.join(MEDIA_ROOT, data_sample.file.path)
                upload_service.copy_file(source_file_path, os.path.join(MEDIA_ROOT, upload_to))
                sp = SellerProductDataSampleArchive(seller_product=seller_product_acrhive, file=upload_to)
                sp.save()

    def _update_data_urls(self, data_urls, seller_product, seller_product_acrhive):
        SellerProductDataUrl.objects.delete_by_seller_product(seller_product=seller_product)
        if data_urls:
            SellerProductDataUrl.objects.bulk_create([
                SellerProductDataUrl(seller_product=seller_product, **du) for du in data_urls
            ])
            SellerProductDataUrlArchive.objects.bulk_create([
                SellerProductDataUrlArchive(seller_product=seller_product_acrhive, **du) for du in data_urls
            ])

    def delete_object(self, seller_product):
        seller_product.delete()
