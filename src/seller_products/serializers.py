from rest_framework import serializers
from seller_products.models import SellerProduct


class SellerProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerProduct
        fields = ['id', 'descr']
