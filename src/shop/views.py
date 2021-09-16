from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from app.response import response_ok
from shop.serializers import SellerProductSerializer
from seller_products.serializers import SellerProductsSerializer
from seller_products.models import SellerProduct
from sellers.serializer import SellerViewSerializer
from categories.models import Category
from django.db.models import Exists, OuterRef
from categories.serializers import CategorySerializer


class ProductCategoriesListView(GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, format=None):
        categories = Category.objects.get_categories_with_products()
        serializer = self.serializer_class(categories, many=True)
        return response_ok({'categories': serializer.data})


class ProductsListView(GenericAPIView):
    serializer_class = SellerProductSerializer

    def get(self, request, format=None):
        params = request.GET.copy()
        category_ids = params.getlist('category_id')
        seller_products = SellerProduct.objects.get_seller_products_by_categories(category_ids)
        serializer = self.serializer_class(seller_products, many=True)
        return response_ok({'seller_products': serializer.data})


class ProductDetailView(GenericAPIView):
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
    serializer_class = SellerProductSerializer

    def get(self, request, seller_product_id, format=None):
        related_products = SellerProduct.objects.get_related_seller_products(seller_product_id)
        serializer = self.serializer_class(related_products, many=True)
        return response_ok({
            'related_products': serializer.data
        })
