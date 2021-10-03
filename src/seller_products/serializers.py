from rest_framework import serializers

from categories.models import Category
from data_delivery_types.models import DataDeliveryType
from geo_regions.models import GeoRegion
from languages.models import Language
from product_data_types.models import DataFormat, DataType
from seller_products.models import SellerProduct, SellerProductDataSample, SellerProductDataUrl
from sellers.models import Seller
from rest_framework import serializers
from rest_framework.fields import UUIDField

from upload.models import UploadedFile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['seller_id', 'name']


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


class DataSampleSerializer(serializers.ModelSerializer):
    uuid = serializers.PrimaryKeyRelatedField(queryset=UploadedFile.objects.all(), write_only=True)
    data_delivery_type_id = serializers.PrimaryKeyRelatedField(queryset=DataDeliveryType.objects.all(), write_only=True, source='data_delivery_type')
    data_format_id = serializers.PrimaryKeyRelatedField(queryset=DataFormat.objects.all(), write_only=True, source='data_format')

    class Meta:
        model = SellerProductDataSample
        fields = ['uuid', 'data_delivery_type_id', 'data_format_id']


class DataUrlsSerializer(serializers.ModelSerializer):
    data_delivery_type_id = serializers.PrimaryKeyRelatedField(queryset=DataDeliveryType.objects.all(), write_only=True, source='data_delivery_type')
    data_format_id = serializers.PrimaryKeyRelatedField(queryset=DataFormat.objects.all(), write_only=True, source='data_format')

    class Meta:
        model = SellerProductDataUrl
        fields = ['url', 'data_delivery_type_id', 'data_format_id']


class SellerProductsSerializer(serializers.ModelSerializer):
    seller = SellerSerializer(read_only=True)
    data_categories_ids = CategorySerializer(read_only=True, many=True)
    data_geo_regions_ids = GeoRegionSerializer(read_only=True, many=True)
    data_langs_ids = LanguageSerializer(read_only=True, many=True)
    data_types_ids = DataTypeSerializer(read_only=True, many=True)
    data_formats_ids = DataFormatSerializer(read_only=True, many=True)
    data_delivery_types_ids = DataDeliveryTypeSerializer(read_only=True, many=True)
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
            'data_categories_ids',
            'data_geo_regions_ids',
            'data_langs_ids',
            'data_types_ids',
            'data_formats_ids',
            'data_delivery_types_ids',
            'data_samples',
            'data_urls',
        ]


class SellerProductsUpdateSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True)
    data_categories_ids = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, many=True)
    data_geo_regions_ids = serializers.PrimaryKeyRelatedField(queryset=GeoRegion.objects.all(), write_only=True, many=True)
    data_langs_ids = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), write_only=True, many=True)
    data_types_ids = serializers.PrimaryKeyRelatedField(queryset=DataType.objects.all(), write_only=True, many=True)
    data_formats_ids = serializers.PrimaryKeyRelatedField(queryset=DataFormat.objects.all(), write_only=True, many=True)
    data_delivery_types_ids = serializers.PrimaryKeyRelatedField(queryset=DataDeliveryType.objects.all(), write_only=True, many=True)
    data_samples = serializers.ListField(child=DataSampleSerializer(), write_only=True, required=False)
    data_urls = serializers.ListField(child=DataUrlsSerializer(), write_only=True, required=False)

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
            'data_categories_ids',
            'data_geo_regions_ids',
            'data_langs_ids',
            'data_types_ids',
            'data_formats_ids',
            'data_delivery_types_ids',
            'data_samples',
            'data_urls'
        ]


class UploadedFilesSerializer(serializers.Serializer):
    data_samples = serializers.PrimaryKeyRelatedField(queryset=UploadedFile.objects.all(), write_only=True, many=True)
