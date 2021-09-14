from django.db import transaction
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from app.response import response_ok
from seller_products.serializers import SellerProductsSerializer, SellerProductsUpdateSerializer
from seller_products.service import SellerProductService
from seller_products.models import SellerProduct


class SellerProductsListView(GenericAPIView, SellerProductService):
    """
    Get list of all products belong to the current user (must be a seller)
    Creates a new product
    URL: `/api/v1/seller-products/my/`
    METHODS: GET, POST
    """
    serializer_class = SellerProductsSerializer
    update_serializer_class = SellerProductsUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        seller_products = SellerProduct.objects.get_products_by_seller_id(request.user.id)
        serializer = self.serializer_class(seller_products, many=True)
        return response_ok({'seller-products': serializer.data})

    def post(self, request, format=None):
        seller = self.get_seller(request.user.id)
        request.data['seller'] = seller.seller_id
        serializer = self.update_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.create_object(serializer.validated_data)
        return response_ok({}, http_code=status.HTTP_200_OK)


class SellerProductsView(APIView, SellerProductService):
    """
    Get, update or delete a single product by specified ID if it belongs to the current user (must be a seller)
    URL: `/api/v1/seller-products/my/`
    METHODS: GET, PUT, DELETE
    """
    serializer_class = SellerProductsSerializer
    update_serializer_class = SellerProductsUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        seller_product = SellerProduct.objects.get_product_by_seller_id(request.user.id)
        serializer = self.serializer_class(seller_product)
        return response_ok(serializer.data)

    def put(self, request, pk, format=None):
        seller_product = self.get_seller_product(pk, request.user.id)
        request.data['seller'] = request.user.id
        serializer = self.update_serializer_class(seller_product, data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            self.update_object(seller_product, serializer.validated_data)
        return response_ok({}, http_code=status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        seller_product = self.get_seller_product(pk, request.user.id)
        self.delete_object(seller_product)
        return response_ok({}, http_code=status.HTTP_204_NO_CONTENT)
