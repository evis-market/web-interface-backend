from rest_framework import serializers

from sales.models import Sale, SaleProduct
from seller_products.models import SellerProductArchive


class SaleProductSerializer(serializers.ModelSerializer):
    sale = serializers.PrimaryKeyRelatedField(queryset=Sale.objects.all())
    seller_product_archive = serializers.PrimaryKeyRelatedField(queryset=SellerProductArchive.objects.all())

    class Meta:
        model = SaleProduct
        fields = [
            'sale',
            'seller_product_archive'
        ]


class SalesSerializer(serializers.ModelSerializer):
    sold_products = SaleProductSerializer(read_only=True, many=True, source='sale_product')

    class Meta:
        model = Sale
        fields = ['created_at', 'uuid', 'seller', 'buyer', 'amount', 'sold_products']
