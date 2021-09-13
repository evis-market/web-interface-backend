from django.db import transaction
from rest_framework.exceptions import APIException, NotFound
from rest_framework.generics import GenericAPIView
from rest_framework import permissions
from rest_framework.views import APIView

from app.response import response_ok, response_err
from app.utils import copy_instance
from seller_products.models import SellerProduct, SellerProductArchive
from seller_products.serializers import SellerProductsSerializer
from seller_products.filters import SellerProductFilter
from seller_products.service import SellerProductMixin
from sellers.models import Seller


class SellerProductsListView(GenericAPIView, SellerProductMixin):
    """
    Get list of all products belong to the current user (must be a seller)
    Creates a new product
    URL: `/api/v1/seller-products/my/`
    METHODS: GET, POST
    """
    serializer_class = SellerProductsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user_id = request.user.id
        seller = Seller.objects.get_seller_by_user_id(user_id)

        if user_id and not Seller.objects.get_seller_by_user_id(user_id):
            raise APIException('The current user is not registered as a Seller', 403)

        queryset = SellerProduct.objects.all()
        seller_product_filter = SellerProductFilter({'seller': seller.id}, queryset=queryset)
        serializer = self.serializer_class(seller_product_filter.qs, many=True)
        return response_ok({'seller-products': serializer.data})

    def post(self, request, format=None):
        seller = self.get_seller(request)

        request.data['seller_id'] = seller.id
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return response_ok(serializer.data)


class SellerProductsView(APIView, SellerProductMixin):
    """
    Get, update or delete a single product by specified ID if it belongs to the current user (must be a seller)
    URL: `/api/v1/seller-products/my/`
    METHODS: GET, PUT, DELETE
    """
    serializer_class = SellerProductsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, seller):
        try:
            return SellerProduct.objects.get_product_by_seller_id(pk=pk, seller=seller)
        except SellerProduct.DoesNotExist:
            raise NotFound(
                f'Either the product not found or '
                f'the current user does not have access permissions to the product'
            )

    def get(self, request, pk, format=None):
        seller = self.get_seller(request)
        seller_product = self.get_object(pk, seller)
        serializer = self.serializer_class(seller_product)
        return response_ok(serializer.data)

    def put(self, request, pk, format=None):
        seller = self.get_seller(request)
        seller_product = self.get_object(pk, seller)
        serializer = self.serializer_class(seller_product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response_ok(serializer.data)

        return response_err(400, serializer.errors)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        # todo: seller_product_archive instance will not be created !
        seller = self.get_seller(request)
        seller_product = self.get_object(pk, seller)
        seller_product.delete()
        return response_ok({}, 204)
