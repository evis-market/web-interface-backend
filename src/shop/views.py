from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from rest_framework.generics import GenericAPIView

from app.response import response_ok
from categories.models import Category
from categories.serializers import CategorySerializer
from data_delivery_types.models import DataDeliveryType
from data_delivery_types.serializers import DataDeliveryTypeSerializer
from geo_regions.models import GeoRegion
from geo_regions.serializers import GeoRegionSerializer
from languages.models import Language
from product_data_types.models import DataFormat, DataType
from product_data_types.serializers import DataFormatSerializer, DataTypeSerializer
from seller_products.models import SellerProduct
from seller_products.serializers import LanguageSerializer, SellerProductsSerializer
from sellers.serializer import SellerViewSerializer
from shop.paginators import ProductsPaginator
from shop.serializers import SellerProductSerializer
from shop.service import ShopService


class ProductCategoriesListView(GenericAPIView):
    """
    URL: `/api/v1/shop/categories/`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "categories": [
            {
              "name": "Category1 name",
              ...
            },
            {
              "name": "Category2 name",
              ...
            }
          ]
        }
    """
    serializer_class = CategorySerializer

    @method_decorator(never_cache)
    def get(self, request, format=None):
        categories = Category.objects.get_categories_with_products()
        serializer = self.serializer_class(categories, many=True)
        return response_ok({'categories': serializer.data})


class ProductsListView(GenericAPIView):
    """
    URL: `/api/v1/shop/products/`

    Method: `GET`

    **URL parameters**

        all filter options:

        category_ids - products category ID, example: 1,2,3
        pagination:

        offset

        limit

        order_by

        valid order_by values: name, -name, 'price_per_one_time', '-price_per_one_time',
        'price_per_month', '-price_per_month', 'price_per_year', '-price_per_year', 'price_by_request',
        '-price_by_request', rating, -rating

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",
          "products": [
            ...
          ]
        }
    """
    serializer_class = SellerProductSerializer
    pagination_class = ProductsPaginator

    def get(self, request, format=None):
        shop_service = ShopService()
        product_name = request.GET.get('name', '')
        category_ids = shop_service.get_category_ids(request)
        order_by_fields = shop_service.get_order_by(request)
        seller_products = shop_service.get_shop_products(product_name, category_ids, order_by_fields)
        seller_products_page = self.paginate_queryset(seller_products)
        serializer = self.serializer_class(seller_products_page, many=True)
        return response_ok({
            'seller_products_count': seller_products.count(),
            'seller_products': serializer.data
        })


class ProductDetailView(GenericAPIView):
    """
    URL: `/api/v1/shop/product/:seller_product_id`

    Method: `GET`

    **URL parameters**

        seller_product_id - seller product ID, example: 1
        Query parameters

        related_products_limit - default 20

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "seller_product": {
            "name": "Product1 name",
            "descr": "Product1 description",
            ...
          },

          "seller": {
            "name": "Seller name",
            "descr": "Seller description",
            "rating": 4.96,
            ...
          }

          "related_products": [
            ...
          ]
        }
    """
    seller_serializer_class = SellerViewSerializer
    seller_product_serializer_class = SellerProductsSerializer

    def get(self, request, seller_product_id, format=None):
        seller_product = SellerProduct.objects.get_seller_product_detailed(seller_product_id)
        related_products = SellerProduct.objects.get_related_seller_products(seller_product_id)
        related_products_serializer = self.seller_product_serializer_class(related_products, many=True)
        seller_serializer = self.seller_serializer_class(seller_product.seller)
        seller_product_serializer = self.seller_product_serializer_class(seller_product)
        return response_ok({
            'seller': seller_serializer.data,
            'seller_product': seller_product_serializer.data,
            'related_products': related_products_serializer.data,
        })


class RelatedProductsListView(GenericAPIView):
    """
    URL: `/api/v1/shop/related_products/:seller_product_id`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "related_products": [
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

          "related_products": []
        }
    """
    serializer_class = SellerProductSerializer
    pagination_class = ProductsPaginator

    def get(self, request, seller_product_id, format=None):
        related_products = SellerProduct.objects.get_related_seller_products(seller_product_id)
        related_products_page = self.paginate_queryset(related_products)
        serializer = self.serializer_class(related_products_page, many=True)
        return response_ok({
            'related_products': serializer.data,
        })


class ProductOptionsListView(GenericAPIView):
    """
    URL: `/api/v1/shop/all_product_options`

    Method: `GET`

    **Successful response**

        HTTP status Code: 200

        {
          "status": "OK",

          "categories": [],
          "langs": [],
          "geo_regions": [],
          "data_types": [],
          "data_formats": [],
          "data_delivery_types": []
        }
    """
    category_serializer = CategorySerializer
    geo_region_serializer = GeoRegionSerializer
    data_delivery_type_serializer = DataDeliveryTypeSerializer
    data_format_serializer = DataFormatSerializer
    data_type_serializer = DataTypeSerializer
    language_serializer = LanguageSerializer

    def get(self, request, format=None):
        categories = Category.objects.get_categories_with_recommended()
        geo_regions = GeoRegion.objects.get_queryset()
        data_delivery_types = DataDeliveryType.objects.get_all()
        data_formats = DataFormat.objects.get_all()
        data_types = DataType.objects.get_all()
        languages = Language.objects.get_all()

        category_serializer = self.category_serializer(categories, many=True)
        geo_regions = self.geo_region_serializer(geo_regions, many=True)
        data_delivery_types = self.data_delivery_type_serializer(data_delivery_types, many=True)
        data_formats = self.data_format_serializer(data_formats, many=True)
        data_types = self.data_type_serializer(data_types, many=True)
        languages = self.language_serializer(languages, many=True)

        return response_ok({
            'categories': category_serializer.data,
            'geo_regions': geo_regions.data,
            'data_delivery_types': data_delivery_types.data,
            'data_formats': data_formats.data,
            'data_types': data_types.data,
            'languages': languages.data,
        })
