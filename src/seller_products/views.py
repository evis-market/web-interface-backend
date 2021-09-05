from django.shortcuts import render
from rest_framework.views import APIView
from seller_products.models import SellerProduct
from seller_products.serializers import SellerProductsSerializer
from app.response import response_ok
from sellers.managers import SellerManager
from sellers.models import Seller


class SellerProductsListView(APIView):
    """

    """
    def get(self, request, format=None):
        seller_products = SellerProduct.objects.filter(
            seller=Seller.objects.get_seller_by_user_id(request.user.id)
        )
        serializer = SellerProductsSerializer(seller_products, many=True)
        return response_ok({'categories': serializer.data})

    def post(self, request, format=None):
        pass


class SellerProductsView(APIView):
    """

    """

    def get(self, request, pk, format=None):
        pass

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass
