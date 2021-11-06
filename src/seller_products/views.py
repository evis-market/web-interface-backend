from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from app.response import response_ok
from seller_products.models import SellerProduct
from seller_products.serializers import SellerProductsSerializer, SellerProductsUpdateSerializer, UploadedFilesSerializer
from seller_products.service import SellerProductService


class SellerProductsListView(GenericAPIView):
    """
    URL: `/api/v1/seller_products/my/`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "products": [
            {
              "name": "Product1 name",
              "descr": "Product1 description",
              ...
            },
            {
              "name": "Product2 name",
              "descr": "Product2 description",
              ...
            }
          ]
        }
    **Successful empty response**

        HTTP status Code: 200

        {
          "status": "OK",

          "products": []
        }

    **Failed response**

        HTTP status Code: 403

        {
          "status": "ERR",

          "error": {
              "code": 403,
              "msg" : "forbidden"
          }
        }

    URL: `/api/v1/seller_products/my/`

    Method: `POST`

    **Request**

        {
          "name": "Product name",
          "descr": "Product description",
          "price_one_time": 99.99,
          "price_per_month": 199,
          "price_per_year": 999,
          "price_by_request": false,
          "price_per_usage": true,
          "price_per_usage_descr": "$10 per 1000 API requests",

          "data_categories_ids": [1, 2, 3],
          "data_langs_ids": [1, 2, 3],
          "data_geo_regions_ids": [1, 2, 3],
          "data_types_ids": [1],
          "data_formats_ids": [1, 2],
          "data_delivery_types_ids": [1, 2],
          "data_urls": [
            { "data_delivery_type_id": 1, "data_format_id": 1, "url": "http://domain.com/data1.xlsx" },
            { "data_delivery_type_id": 1, "data_format_id": 2, "url": "http://domain.com/data1.xml" }
          ],
          "data_sample_urls": [
            "http://domain.com/data_sample1.xls",
            "http://domain.com/data_sample2.xls"
          ]
        }

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK"
        }

    **Failed response**

        HTTP status Code: 400

        {
          "status": "ERR",

          "error": {
              "code": 400,
              "msg" : "bad request",

              "invalid_fields": {
                "name": "required field",
                "descr": "to long, 300 symbols maximum",
                "data_urls": [
                    { "data_delivery_type_id": 1, "data_format_id": 1, "error": "invalid format" }
                ]
              }
          }
        }
    """
    serializer_class = SellerProductsSerializer
    uploaded_files_serializer = UploadedFilesSerializer
    update_serializer_class = SellerProductsUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        seller_products = SellerProduct.objects.get_products_by_seller_id(request.user.id)
        serializer = self.serializer_class(seller_products, many=True, context={'request': request})
        return response_ok({'seller-products': serializer.data})

    def post(self, request, format=None):
        seller_product_service = SellerProductService()
        seller = seller_product_service.get_seller(request.user.id)
        request.data['seller'] = seller.seller_id
        serializer = self.update_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            seller_product_service.create_object(serializer.validated_data)

        return response_ok({}, http_code=status.HTTP_200_OK)


class SellerProductsView(APIView):
    """
    URL: `/api/v1/seller_products/my/:seller_product_id`

    Method: `GET`

    URL parameters

    seller_product_id - seller product ID, example: 1

    **Successful response**
        HTTP status Code: 200

        {
          "status": "OK",

          "product": {
            "name": "Product1 name",
            "descr": "Product1 description",
            ...
          }
        }
    **Failed response**
        HTTP status Code: 401

        {
          "status": "ERR",

          "error": {
              "code": 401,
              "msg" : "unauthorized"
          }
        }

    URL: `/api/v1/seller_products/my/`

    Method: `PUT`

    **Request**

        {
          "name": "Product name",
          "descr": "Product description",
          "price_one_time": 99.99,
          "price_per_month": 199,
          "price_per_year": 999,
          "price_by_request": false,
          "price_per_usage": true,
          "price_per_usage_descr": "$10 per 1000 API requests",

          "data_categories_ids": [1, 2, 3],
          "data_langs_ids": [1, 2, 3],
          "data_geo_regions_ids": [1, 2, 3],
          "data_types_ids": [1],
          "data_formats_ids": [1, 2],
          "data_delivery_types_ids": [1, 2],
          "data_urls": [
            { "data_delivery_type_id": 1, "data_format_id": 1, "url": "http://domain.com/data1.xlsx" },
            { "data_delivery_type_id": 1, "data_format_id": 2, "url": "http://domain.com/data1.xml" }
          ],
          "data_samples": [
            "06ed84be-0eac-42a6-9020-213329db3737",
            "4f41af44-6f82-48b1-ba97-c86f5469ce04"
          ]
        }
    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK"
        }
    **Failed response**

        HTTP status Code: 400

        {
          "status": "ERR",

          "error": {
              "code": 400,
              "msg" : "bad request",

              "invalid_fields": {
                "name": "required field",
                "descr": "to long, 300 symbols maximum",
                "data_urls": [
                    { "data_delivery_type_id": 1, "data_format_id": 1, "error": "invalid format" }
                ]
              }
          }
        }

    URL: `/api/v1/seller_products/my/:seller_product_id`

    Method: `DELETE`

    **Successful response**

        HTTP status Code: 204

        {
          "status": "OK"
        }

    **Failed response**

        HTTP status Code: 403

        {
          "status": "ERR",

          "error": {
              "code": 403,
              "msg" : "Forbidden"
          }
        }
    """
    serializer_class = SellerProductsSerializer
    update_serializer_class = SellerProductsUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        seller_product = SellerProduct.objects.get_product_by_seller_id(pk, request.user.id)
        serializer = self.serializer_class(seller_product, context={'request': request})
        return response_ok(serializer.data)

    def put(self, request, pk, format=None):
        seller_product_service = SellerProductService()
        seller_product = seller_product_service.get_seller_product(pk, request.user.id)
        request.data['seller'] = request.user.id
        serializer = self.update_serializer_class(seller_product, data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            seller_product_service.update_object(seller_product, serializer.validated_data)
        return response_ok({}, http_code=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        seller_product_service = SellerProductService()
        seller_product = seller_product_service.get_seller_product(pk, request.user.id)
        seller_product_service.delete_object(seller_product)
        return response_ok({}, http_code=status.HTTP_204_NO_CONTENT)
