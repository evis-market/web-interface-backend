import pytest
from django.core.files import File
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from seller_products.models import SellerProduct, SellerProductDataSample, SellerProductDataUrl
from seller_products.views import SellerProductsListView
from sellers.models import Seller
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

