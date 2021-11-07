import json

import pytest
from django.core.files import File
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from seller_products.models import SellerProduct, SellerProductDataSample, SellerProductDataUrl, SellerProductDataSampleArchive, SellerProductDataUrlArchive, \
    SellerProductArchive
from seller_products.views import SellerProductsListView
from sellers.models import Seller
from upload.models import UploadedFile
from users.models import User

pytestmark = pytest.mark.django_db


class TestSellerProductsListView:

    def test_get_empty(self):
        """
        Test: get without any seller-products
        """
        user = mixer.blend(User)
        url = reverse('SellerProductsView')
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = SellerProductsListView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        assert response.data['products'] == []

    def test_get(self, data_formats, data_delivery_types):
        """
        Test: get seller-products
        """
        user = mixer.blend(User)
        seller = mixer.blend(Seller,
                             seller=user,
                             logo=None)

        seller_product_1 = mixer.blend(SellerProduct,
                                       seller=seller,
                                       name='seller_product_1',
                                       descr='seller_product_1_description',
                                       price_per_one_time=1.1,
                                       price_per_month=12.1,
                                       price_per_year=123.1,
                                       price_by_request=True,
                                       price_per_usage=True,
                                       price_per_usage_descr="$10 per 1000 requests",
                                       rating=1.1)
        # seller_product_data_sample_1
        mixer.blend(SellerProductDataSample,
                    seller_product=seller_product_1,
                    file=File(open('test-files/test-file-1.py', 'rb')),
                    data_delivery_type=data_delivery_types[0],
                    data_format=data_formats[0])
        # seller_product_data_url_1
        mixer.blend(SellerProductDataUrl,
                    seller_product=seller_product_1,
                    url='http://127.0.0.1:8000/',
                    data_delivery_type=data_delivery_types[0],
                    data_format=data_formats[0])
        # seller_product_2
        mixer.blend(SellerProduct,
                    seller=seller,
                    name='seller_product_2',
                    descr='seller_product_2_description',
                    price_per_one_time=12.2,
                    price_per_month=12.2,
                    price_per_year=123.2,
                    price_by_request=False,
                    price_per_usage=False,
                    price_per_usage_descr="",
                    rating=2.2)

        url = reverse('SellerProductsView')
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = SellerProductsListView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        must_exists_fields = ['id', 'name', 'descr', 'price_per_one_time', 'price_per_month', 'price_per_year', 'price_by_request',
                              'price_per_usage', 'price_per_usage_descr', 'rating', 'data_urls']
        for product in response.data['products']:
            for field in must_exists_fields:
                assert field in product

    def test_post(self, categories, geo_regions, languages, data_types, data_formats, data_delivery_types):
        user = mixer.blend(User)
        # seller
        mixer.blend(Seller,
                    seller=user,
                    logo=None)
        uploaded_file = mixer.blend(
            UploadedFile,
            file=File(open('test-files/test-file-1.py', 'rb')),
            file_name_original='test-file-1',
            created_by=user)

        request_data = {
            "name": "Product name",
            "descr": "Product description",
            "price_one_time": 99.99,
            "price_per_month": 199,
            "price_per_year": 999,
            "price_by_request": False,
            "price_per_usage": True,
            "price_per_usage_descr": "$10 per 1000 API requests",
            "data_categories_ids": [1, 2],
            "data_langs_ids": [1, 2],
            "data_geo_regions_ids": [1, 2],
            "data_types_ids": [1, 2],
            "data_formats_ids": [1, 2],
            "data_delivery_types_ids": [1, 2],
            "data_urls": [
                {"data_delivery_type_id": 1, "data_format_id": 1, "url": "http://domain.com/data1.xlsx"},
                {"data_delivery_type_id": 2, "data_format_id": 2, "url": "http://domain.com/data1.xml"}
            ],
            "data_samples": [
                str(uploaded_file.uuid)
            ]
        }
        # checking that the database is clear
        assert len(SellerProduct.objects.all()) == 0
        assert len(SellerProductArchive.objects.all()) == 0
        assert len(SellerProductDataSample.objects.all()) == 0
        assert len(SellerProductDataSampleArchive.objects.all()) == 0
        assert len(SellerProductDataUrl.objects.all()) == 0
        assert len(SellerProductDataUrlArchive.objects.all()) == 0

        url = reverse('SellerProductsView')
        request = APIRequestFactory().post(url, data=json.dumps(request_data), content_type='application/json')
        force_authenticate(request, user=user)
        response = SellerProductsListView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'

        # checking that all instances are created
        seller_product = SellerProduct.objects.get(name=request_data['name'])
        seller_product_archive = SellerProductArchive.objects.get(name=request_data['name'])

        seller_product_data_sample = SellerProductDataSample.objects.get(seller_product=seller_product)
        seller_product_data_sample_archive = SellerProductDataSampleArchive.objects.get(seller_product=seller_product_archive)
        assert seller_product_data_sample.get_filename_without_extension == str(uploaded_file.uuid)
        assert str(seller_product_data_sample_archive.file).split('/')[1] == str(seller_product_data_sample.file).split('/')[1]

        SellerProductDataUrl.objects.get(seller_product=seller_product, url=request_data['data_urls'][0]['url'])
        SellerProductDataUrl.objects.get(seller_product=seller_product, url=request_data['data_urls'][1]['url'])

        SellerProductDataUrlArchive.objects.get(seller_product=seller_product_archive, url=request_data['data_urls'][0]['url'])
        SellerProductDataUrlArchive.objects.get(seller_product=seller_product_archive, url=request_data['data_urls'][1]['url'])
