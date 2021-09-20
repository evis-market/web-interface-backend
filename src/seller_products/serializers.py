from rest_framework import serializers

from categories.models import Category
from data_delivery_types.models import DataDeliveryType
from geo_regions.models import GeoRegion
from languages.models import Language
from product_data_types.models import DataFormat, DataType
from seller_products.models import SellerProduct, SellerProductDataSample, SellerProductDataUrl
from sellers.models import Seller


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['seller_id', 'name']


class DataSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProductDataSample
        fields = ['url', 'data_type', 'data_format']


class DataUrlsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProductDataUrl
        fields = ['url', 'data_type', 'data_format']


class GeoRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoRegion
        fields = ['id', 'name', 'iso_code']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name_native', 'name_en', 'slug']


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = ['id', 'name']


class DataFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFormat
        fields = ['id', 'name']


class DataDeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataDeliveryType
        fields = ['id', 'name']


class SellerProductsSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    categories = CategorySerializer(read_only=True, many=True)
    geo_regions = GeoRegionSerializer(read_only=True, many=True)
    languages = LanguageSerializer(read_only=True, many=True)
    data_type = DataTypeSerializer(read_only=True, many=True)
    data_format = DataFormatSerializer(read_only=True, many=True)
    data_delivery_type = DataDeliveryTypeSerializer(read_only=True, many=True)
    data_samples = DataSampleSerializer(read_only=True, many=True)
    data_urls = DataUrlsSerializer(read_only=True, many=True)

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
            'seller',
            'categories',
            'geo_regions',
            'languages',
            'data_type',
            'data_format',
            'data_delivery_type',
            'data_samples',
            'data_urls',
        ]


class SellerProductsUpdateSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, many=True)
    geo_regions = serializers.PrimaryKeyRelatedField(queryset=GeoRegion.objects.all(), write_only=True, many=True)
    languages = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), write_only=True, many=True)
    data_types = serializers.PrimaryKeyRelatedField(queryset=DataType.objects.all(), write_only=True, many=True)
    data_formats = serializers.PrimaryKeyRelatedField(queryset=DataFormat.objects.all(), write_only=True, many=True)
    data_delivery_types = serializers.PrimaryKeyRelatedField(queryset=DataDeliveryType.objects.all(), write_only=True, many=True)
    data_samples = serializers.ListField(child=DataSampleSerializer(), write_only=True)
    data_urls = serializers.ListField(child=DataUrlsSerializer(), write_only=True)

    class Meta:
        model = SellerProduct
        fields = [
            'name',
            'descr',
            'price_per_one_time',
            'price_per_month',
            'price_per_year',
            'price_by_request',
            'price_per_usage',
            'price_per_usage_descr',
            'seller',
            'categories',
            'geo_regions',
            'languages',
            'data_types',
            'data_formats',
            'data_delivery_types',
            'data_samples',
            'data_urls'
        ]
