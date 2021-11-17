import pytest
from django.core.files import File
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate

from categories.models import Category
from seller_products.models import SellerProduct, SellerProductDataSample, SellerProductDataUrl
from sellers.models import Seller
from shop.views import ProductsListView, ProductDetailView, RelatedProductsListView, ProductOptionsListView
from users.models import User

pytestmark = pytest.mark.django_db


class TestSellerSettingsView:

    def test_get_products(self):
        """
        Test: get products
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
        seller_product_2 = mixer.blend(SellerProduct,
                                       seller=seller,
                                       name='seller_product_2',
                                       descr='seller_product_2_description',
                                       price_per_one_time=2.1,
                                       price_per_month=22.1,
                                       price_per_year=223.1,
                                       price_by_request=False,
                                       price_per_usage=False,
                                       price_per_usage_descr="",
                                       rating=2.1)
        url = reverse('Products')
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = ProductsListView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        assert response.data['seller_products_count'] == 2

        assert response.data["seller_products"][0]["id"] == seller_product_1.id
        assert response.data["seller_products"][0]["name"] == seller_product_1.name
        assert response.data["seller_products"][0]["descr"] == seller_product_1.descr
        assert response.data["seller_products"][0]["price_per_one_time"] == seller_product_1.price_per_one_time
        assert response.data["seller_products"][0]["price_per_month"] == seller_product_1.price_per_month
        assert response.data["seller_products"][0]["price_per_year"] == seller_product_1.price_per_year
        assert response.data["seller_products"][0]["price_by_request"] == seller_product_1.price_by_request
        assert response.data["seller_products"][0]["price_per_usage"] == seller_product_1.price_per_usage
        assert response.data["seller_products"][0]["price_per_usage_descr"] == seller_product_1.price_per_usage_descr
        assert response.data["seller_products"][0]["rating"] == seller_product_1.rating

        assert response.data["seller_products"][1]["id"] == seller_product_2.id
        assert response.data["seller_products"][1]["name"] == seller_product_2.name
        assert response.data["seller_products"][1]["descr"] == seller_product_2.descr
        assert response.data["seller_products"][1]["price_per_one_time"] == seller_product_2.price_per_one_time
        assert response.data["seller_products"][1]["price_per_month"] == seller_product_2.price_per_month
        assert response.data["seller_products"][1]["price_per_year"] == seller_product_2.price_per_year
        assert response.data["seller_products"][1]["price_by_request"] == seller_product_2.price_by_request
        assert response.data["seller_products"][1]["price_per_usage"] == seller_product_2.price_per_usage
        assert response.data["seller_products"][1]["price_per_usage_descr"] == seller_product_2.price_per_usage_descr
        assert response.data["seller_products"][1]["rating"] == seller_product_2.rating

    def test_get_products_detail(self, data_delivery_types, data_formats, categories):
        """
        Test: get product detail
        """
        user = mixer.blend(User)
        seller = mixer.blend(Seller,
                             seller=user,
                             logo=None)
        seller_product = mixer.blend(SellerProduct,
                                     seller=seller,
                                     name='seller_product_1',
                                     descr='seller_product_1_description',
                                     price_per_one_time=1.1,
                                     price_per_month=12.1,
                                     price_per_year=123.1,
                                     price_by_request=True,
                                     price_per_usage=True,
                                     price_per_usage_descr="$10 per 1000 requests",
                                     rating=1.1,
                                     categories=categories[0])
        related_seller_product = mixer.blend(SellerProduct,
                                             seller=seller,
                                             name='seller_product_2',
                                             descr='seller_product_2_description',
                                             price_per_one_time=12.2,
                                             price_per_month=12.2,
                                             price_per_year=123.2,
                                             price_by_request=False,
                                             price_per_usage=False,
                                             price_per_usage_descr="",
                                             rating=2.2,
                                             categories=categories[0])
        seller_product_data_sample = mixer.blend(SellerProductDataSample,
                                                 seller_product=seller_product,
                                                 file=File(open('app/test-files/test-file-1.py', 'rb')),
                                                 data_delivery_type=data_delivery_types[0],
                                                 data_format=data_formats[0])
        seller_product_data_url = mixer.blend(SellerProductDataUrl,
                                              seller_product=seller_product,
                                              url='http://127.0.0.1:8000/',
                                              data_delivery_type=data_delivery_types[0],
                                              data_format=data_formats[0])
        url = reverse('ProductDetail', kwargs={"seller_product_id": seller_product.id})
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = ProductDetailView.as_view()(request=request, seller_product_id=seller_product.id)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'

        assert response.data["seller_product"]["id"] == seller_product.id
        assert response.data["seller_product"]["name"] == seller_product.name
        assert response.data["seller_product"]["descr"] == seller_product.descr
        assert response.data["seller_product"]["price_per_one_time"] == seller_product.price_per_one_time
        assert response.data["seller_product"]["price_per_month"] == seller_product.price_per_month
        assert response.data["seller_product"]["price_per_year"] == seller_product.price_per_year
        assert response.data["seller_product"]["price_by_request"] == seller_product.price_by_request
        assert response.data["seller_product"]["price_per_usage"] == seller_product.price_per_usage
        assert response.data["seller_product"]["price_per_usage_descr"] == seller_product.price_per_usage_descr
        assert response.data["seller_product"]["rating"] == seller_product.rating
        assert response.data["seller_product"]["seller"]['seller_id'] == seller_product.seller.seller.id
        assert response.data["seller_product"]["seller"]['name'] == seller_product.seller.name
        assert response.data["seller_product"]["data_samples"][0]["file_url"] == f'http://testserver/media/{seller_product_data_sample.file}'
        assert response.data["seller_product"]["data_urls"][0]["url"] == seller_product_data_url.url

        assert response.data["seller"]["name"] == seller.name
        assert response.data["seller"]["descr"] == seller.descr
        assert response.data["seller"]["logo_url"] == str(seller.logo)
        assert response.data["seller"]["wallet_for_payments_erc20"] == seller.wallet_for_payments_erc20
        assert response.data["seller"]["rating"] == seller.rating
        assert response.data["seller"]["contacts"] == list(seller.contacts())

        assert len(response.data['related_products']) == 1
        assert response.data["related_products"][0]["id"] == related_seller_product.id
        assert response.data["related_products"][0]["name"] == related_seller_product.name
        assert response.data["related_products"][0]["descr"] == related_seller_product.descr
        assert response.data["related_products"][0]["price_per_one_time"] == related_seller_product.price_per_one_time
        assert response.data["related_products"][0]["price_per_month"] == related_seller_product.price_per_month
        assert response.data["related_products"][0]["price_per_year"] == related_seller_product.price_per_year
        assert response.data["related_products"][0]["price_by_request"] == related_seller_product.price_by_request
        assert response.data["related_products"][0]["price_per_usage"] == related_seller_product.price_per_usage
        assert response.data["related_products"][0]["price_per_usage_descr"] == related_seller_product.price_per_usage_descr
        assert response.data["related_products"][0]["rating"] == related_seller_product.rating

    def test_get_related_products(self, categories):
        """
        Test: get product detail
        """
        user = mixer.blend(User)
        seller = mixer.blend(Seller,
                             seller=user,
                             logo=None)
        seller_product = mixer.blend(SellerProduct,
                                     seller=seller,
                                     name='seller_product_1',
                                     descr='seller_product_1_description',
                                     price_per_one_time=1.1,
                                     price_per_month=12.1,
                                     price_per_year=123.1,
                                     price_by_request=True,
                                     price_per_usage=True,
                                     price_per_usage_descr="$10 per 1000 requests",
                                     rating=1.1,
                                     categories=categories[0])
        related_seller_product = mixer.blend(SellerProduct,
                                             seller=seller,
                                             name='seller_product_2',
                                             descr='seller_product_2_description',
                                             price_per_one_time=12.2,
                                             price_per_month=12.2,
                                             price_per_year=123.2,
                                             price_by_request=False,
                                             price_per_usage=False,
                                             price_per_usage_descr="",
                                             rating=2.2,
                                             categories=categories[0])
        url = reverse('RelatedProducts', kwargs={"seller_product_id": seller_product.id})
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = RelatedProductsListView.as_view()(request=request, seller_product_id=seller_product.id)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'

        assert len(response.data["related_products"]) == 1
        assert response.data["related_products"][0]["id"] == related_seller_product.id
        assert response.data["related_products"][0]["name"] == related_seller_product.name
        assert response.data["related_products"][0]["descr"] == related_seller_product.descr
        assert response.data["related_products"][0]["price_per_one_time"] == related_seller_product.price_per_one_time
        assert response.data["related_products"][0]["price_per_month"] == related_seller_product.price_per_month
        assert response.data["related_products"][0]["price_per_year"] == related_seller_product.price_per_year
        assert response.data["related_products"][0]["price_by_request"] == related_seller_product.price_by_request
        assert response.data["related_products"][0]["price_per_usage"] == related_seller_product.price_per_usage
        assert response.data["related_products"][0]["price_per_usage_descr"] == related_seller_product.price_per_usage_descr
        assert response.data["related_products"][0]["rating"] == related_seller_product.rating

    def test_get_all_options(self, categories, geo_regions, languages, data_types, data_formats, data_delivery_types):
        user = mixer.blend(User)
        url = reverse('AllOptions')
        request = APIRequestFactory().get(url)
        force_authenticate(request, user=user)
        response = ProductOptionsListView.as_view()(request=request)
        assert response.status_code == 200
        assert response.data['status'] == 'OK'
        assert len(response.data) == 7

        assert len(response.data['categories']) == 2
        for field in ['id', 'parent_id', 'name', 'short_descr', 'descr', 'logo_url', 'slug', 'sort_id', 'recommended_for']:
            assert field in response.data["categories"][0]

        assert len(response.data['geo_regions']) == 3
        for field in ['id', 'name', 'parent_id', 'iso_code']:
            assert field in response.data['geo_regions'][0]

        assert len(response.data['data_delivery_types']) == 2
        for field in ['id', 'name']:
            assert field in response.data['data_delivery_types'][0]

        assert len(response.data['data_types']) == 2
        for field in ['id', 'name']:
            assert field in response.data['data_types'][0]

        assert len(response.data['data_formats']) == 2
        for field in ['id', 'name', 'data_type_id']:
            assert field in response.data['data_formats'][0]

        assert len(response.data['languages']) == 2
        for field in ['id', 'name_native', 'name_en', 'slug']:
            assert field in response.data['languages'][0]
