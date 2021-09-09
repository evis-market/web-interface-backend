from rest_framework.views import APIView

from app.response import response_ok
from seller_products.models import SellerProduct
from seller_products.serializers import SellerProductsSerializer
from sellers.models import Seller
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import permissions


class SellerProductsListView(GenericAPIView):
    """

    """
    serializer_class = SellerProductsSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        seller_products = SellerProduct.objects.filter(
            seller=Seller.objects.get_seller_by_user_id(request.user.id),
        )
        serializer = self.serializer_class(seller_products, many=True)
        return response_ok({'seller-products': serializer.data})

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return response_ok(serializer.data)


class SellerProductsView(APIView):
    """

    """

    def get(self, request, pk, format=None):
        pass

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass
