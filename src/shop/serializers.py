from rest_framework import serializers

from seller_products.models import SellerProduct


class SellerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProduct
        fields = [
            'id',
            'name',
            'descr',
            'price_per_one_time',
            'price_per_month',
            'price_per_year',
            'price_by_request',
            'price_per_usage',
            'price_per_usage_descr',
            'rating',
        ]
