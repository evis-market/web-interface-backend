from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from app.response import response_ok
from shop.serializers import SellerProductSerializer
from seller_products.serializers import SellerProductsSerializer
from seller_products.models import SellerProduct

from sellers.serializer import SellerViewSerializer


class ProductDetailView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
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
        }, 200)


class RelatedProductsListView(GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = SellerProductSerializer

    def get(self, request, seller_product_id, format=None):
        related_products = SellerProduct.objects.get_related_seller_products(seller_product_id)
        serializer = self.serializer_class(related_products, many=True)
        return response_ok({'related_products': serializer.data}, 200)
