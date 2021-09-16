from rest_framework import serializers

from geo_regions.serializers import GeoRegionSerializer
from seller_products.models import SellerProduct
from seller_products.serializers import CategorySerializer
from sellers.serializer import SellerViewSerializer


class SellerProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)

    class Meta:
        model = SellerProduct
        fields = [
            'id',
            'name',
            'descr',
            'categories'
        ]
