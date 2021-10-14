from rest_framework import serializers

from sales.models import Sale
from seller_products.serializers import SellerProductsSerializer
from seller_products.models import SellerProductArchive


class SellerProductsArchiveSerializer(SellerProductsSerializer):

    class Meta:
        model = SellerProductArchive
        fields = [
            'id',
            'name'
        ]


class SalesSerializer(serializers.ModelSerializer):
    products = SellerProductsSerializer(read_only=True, many=True)

    class Meta:
        model = Sale
        fields = ['created_at', 'uuid', 'seller', 'buyer', 'amount', 'products']
