from rest_framework import serializers

from sales.models import Sale, SaleProduct
from seller_products.models import SellerProductArchive
from sellers.models import Seller
from users.models import User


class SellerProductArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProductArchive
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
            'total_reviews_cnt',
            'version'
        ]


class SaleProductSerializer(serializers.ModelSerializer):
    sale = serializers.PrimaryKeyRelatedField(queryset=Sale.objects.all())
    seller_product_archive = SellerProductArchiveSerializer()

    class Meta:
        model = SaleProduct
        fields = [
            'sale',
            'seller_product_archive'
        ]


class SellerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='seller.id')
    first_name = serializers.CharField(source='seller.first_name')
    last_name = serializers.CharField(source='seller.last_name')

    class Meta:
        model = Seller
        fields = [
            'id',
            'first_name',
            'last_name',
            'logo_url'
        ]


class ShoppingListSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    products = SaleProductSerializer(read_only=True, many=True, source='sale_product')

    class Meta:
        model = Sale
        fields = [
            'created_at',
            'uuid',
            'amount',
            'seller',
            'products'
        ]


class BuyerSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    wallet_erc20 = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'uuid',
            'first_name',
            'last_name',
            'wallet_erc20'
        ]


class SellerSalesListSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer(read_only=True)
    products = SaleProductSerializer(read_only=True, many=True, source='sale_product')

    class Meta:
        model = Sale
        fields = [
            'created_at',
            'uuid',
            'amount',
            'buyer',
            'products'
        ]
