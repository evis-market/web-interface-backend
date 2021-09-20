from rest_framework.generics import GenericAPIView

from app.response import response_ok
from categories.models import Category
from categories.serializers import CategorySerializer
from data_delivery_types.models import DataDeliveryType
from data_delivery_types.serializers import DataDeliveryTypeSerializer
from geo_regions.models import GeoRegion
from geo_regions.serializers import GeoRegionSerializer
from product_data_types.models import DataFormat, DataType
from product_data_types.serializers import DataFormatSerializer, DataTypeSerializer
from seller_products.models import SellerProduct
from seller_products.serializers import SellerProductsSerializer
from sellers.serializer import SellerViewSerializer
from shop.serializers import SellerProductSerializer
from shop.paginators import ProductsPaginator
from shop.service import ShopService


class ProductCategoriesListView(GenericAPIView):
    """
    Displaying categories that has at least one product
    URL: `/api/v1/shop/categories/`
    METHODS: GET
    """
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        categories = Category.objects.get_categories_with_products()
        serializer = self.serializer_class(categories, many=True)
        return response_ok({'categories': serializer.data})


class ProductsListView(GenericAPIView, ShopService):
    """
    Displaying products by applied filters on product categories
    URL: `/api/v1/shop/products/`
    METHODS: GET
    """
    serializer_class = SellerProductSerializer
    pagination_class = ProductsPaginator
    order_by_allowed_fields = [
        'id', '-id', 'name', '-name', 'rating', '-rating', 'price_per_one_time', '-price_per_one_time',
        'price_per_month', '-price_per_month', 'price_per_year', '-price_per_year', 'price_by_request',
        '-price_by_request'
    ]

    def get(self, request, format=None):
        seller_products = self.get_shop_products(
            request.GET.getlist('category_id'), request.GET.getlist('order_by'), self.order_by_allowed_fields
        )
        seller_products_page = self.paginate_queryset(seller_products)
        serializer = self.serializer_class(seller_products_page, many=True)
        return response_ok(
            {
                'seller_products_count': seller_products.count(),
                'seller_products': serializer.data
            },
        )


class ProductDetailView(GenericAPIView):
    """
    Displaying detailed product information
    URL: `/api/v1/shop/product/<int:seller_product_id>`
    METHODS: GET
    """
    seller_serializer_class = SellerViewSerializer
    seller_product_serializer_class = SellerProductsSerializer

    def get(self, request, seller_product_id, format=None):
        seller_product = SellerProduct.objects.get_seller_product_detailed(seller_product_id)
        seller = seller_product.seller
        seller_serializer = self.seller_serializer_class(seller)
        seller_product_serializer = self.seller_product_serializer_class(seller_product)
        return response_ok({
            'seller': seller_serializer.data,
            'seller_product': seller_product_serializer.data,
        })


class RelatedProductsListView(GenericAPIView):
    """
    Displaying related products of the specified product.
    Products are related if they share at least one category or descendant category
    URL: `/api/v1/shop/related_products/<int:seller_product_id>`
    METHODS: GET
    """
    serializer_class = SellerProductSerializer

    def get(self, request, seller_product_id, format=None):
        related_products = SellerProduct.objects.get_related_seller_products(seller_product_id)
        serializer = self.serializer_class(related_products, many=True)
        return response_ok({
            'related_products': serializer.data,
        })


class ProductOptionsListView(GenericAPIView):
    """
    Displaying all filter options available for products
    URL: `/api/v1/shop/all_options`
    METHODS: GET
    """
    category_serializer = CategorySerializer
    geo_region_serializer = GeoRegionSerializer
    data_delivery_type_serializer = DataDeliveryTypeSerializer
    data_format_serializer = DataFormatSerializer
    data_type_serializer = DataTypeSerializer

    def get(self, request, format=None):
        categories = Category.objects.get_queryset()
        geo_regions = GeoRegion.objects.get_queryset()
        data_delivery_types = DataDeliveryType.objects.get_all()
        data_formats = DataFormat.objects.get_all()
        data_types = DataType.objects.get_all()

        category_serializer = self.category_serializer(categories, many=True)
        geo_regions = self.geo_region_serializer(geo_regions, many=True)
        data_delivery_types = self.data_delivery_type_serializer(data_delivery_types, many=True)
        data_formats = self.data_format_serializer(data_formats, many=True)
        data_types = self.data_type_serializer(data_types, many=True)

        return response_ok({
            'categories': category_serializer.data,
            'geo_regions': geo_regions.data,
            'data_delivery_types': data_delivery_types.data,
            'data_formats': data_formats.data,
            'data_types': data_types.data,
        })
