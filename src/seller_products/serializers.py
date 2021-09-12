from django.db import transaction
from rest_framework import serializers

from data_delivery_types.models import DataDeliveryType
from product_data_types.models import DataType, DataFormat
from seller_products.models import SellerProduct, SellerProductArchive, SellerProductDataSample, SellerProductDataUrl
from categories.models import Category
from geo_regions.models import GeoRegion
from sellers.models import Seller
from app.utils import copy_instance


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
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True, required=False)
    categories = CategorySerializer(read_only=True, many=True)
    categories_ids = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True, many=True)
    geo_regions = GeoRegionSerializer(read_only=True, many=True)
    geo_regions_ids = serializers.PrimaryKeyRelatedField(queryset=GeoRegion.objects.all(), write_only=True, many=True)
    data_type = DataTypeSerializer(read_only=True, many=True)
    data_type_ids = serializers.PrimaryKeyRelatedField(queryset=DataType.objects.all(), write_only=True, many=True)
    data_format = DataFormatSerializer(read_only=True, many=True)
    data_format_ids = serializers.PrimaryKeyRelatedField(queryset=DataFormat.objects.all(), write_only=True, many=True)
    data_delivery_type = DataDeliveryTypeSerializer(read_only=True, many=True)
    data_delivery_type_ids = serializers.PrimaryKeyRelatedField(queryset=DataDeliveryType.objects.all(), write_only=True, many=True)

    data_samples = DataSampleSerializer(read_only=True, many=True)
    data_samples_objects = serializers.ListField(child=DataSampleSerializer(), write_only=True)
    data_urls = DataUrlsSerializer(read_only=True, many=True)
    data_urls_objects = serializers.ListField(child=DataUrlsSerializer(), write_only=True)

    class Meta:
        model = SellerProduct
        fields = [
            'id',
            'name',
            'descr',
            'seller',
            'seller_id',
            'categories',
            'categories_ids',
            'geo_regions',
            'geo_regions_ids',
            'data_type',
            'data_type_ids',
            'data_format',
            'data_format_ids',
            'data_delivery_type',
            'data_delivery_type_ids',
            'data_samples_objects',
            'data_samples',
            'data_urls_objects',
            'data_urls',
        ]

    @transaction.atomic
    def create(self, validated_data):
        seller = validated_data.pop('seller_id')
        categories = validated_data.pop('categories_ids')
        data_samples = validated_data.pop('data_samples_objects')
        data_urls = validated_data.pop('data_urls_objects')
        geo_regions = validated_data.pop('geo_regions_ids')
        data_type = validated_data.pop('data_type_ids')
        data_format = validated_data.pop('data_format_ids')
        data_delivery_type = validated_data.pop('data_delivery_type_ids')

        seller_product = SellerProduct.objects.create(seller=seller, **validated_data)

        # add m2m fields
        seller_product.categories.add(*categories)
        seller_product.geo_regions.add(*geo_regions)
        seller_product.data_types.add(*data_type)
        seller_product.data_formats.add(*data_format)
        seller_product.data_delivery_types.add(*data_delivery_type)

        # create one to many related objects
        SellerProductDataSample.objects.bulk_create([
            SellerProductDataSample(
                seller_product=seller_product, url=ds['url'], data_type=ds['data_type'], data_format=ds['data_format']
            ) for ds in data_samples
        ])
        SellerProductDataUrl.objects.bulk_create([
            SellerProductDataUrl(
                seller_product=seller_product, url=du['url'], data_type=du['data_type'], data_format=du['data_format']
            ) for du in data_urls
        ])

        # create a copy of instance and all its related data to SellerProductArchive model instance
        seller_product_archive = SellerProductArchive()
        seller_product_archive = copy_instance(seller_product, seller_product_archive)
        seller_product_archive.save()

        return seller_product

    @transaction.atomic
    def update(self, instance, validated_data):
        categories = validated_data.pop('categories_ids')
        data_samples = validated_data.pop('data_samples_objects')
        data_urls = validated_data.pop('data_urls_objects')
        geo_regions = validated_data.pop('geo_regions_ids')
        data_type = validated_data.pop('data_type_ids')
        data_format = validated_data.pop('data_format_ids')
        data_delivery_type = validated_data.pop('data_delivery_type_ids')

        # update regular attributes
        for column, column_value in validated_data.items():
            setattr(instance, column, column_value)
        instance.version = SellerProduct.objects.get(pk=instance.pk).version + 1

        # update m2m fields
        instance.categories.clear()
        instance.categories.add(*categories)
        instance.geo_regions.clear()
        instance.geo_regions.add(*geo_regions)
        instance.data_types.clear()
        instance.data_types.add(*data_type)
        instance.data_formats.add(*data_format)
        instance.data_delivery_types.add(*data_delivery_type)

        # update one to many related objects
        SellerProductDataSample.objects.filter(seller_product=instance).delete()
        SellerProductDataUrl.objects.filter(seller_product=instance).delete()
        SellerProductDataSample.objects.bulk_create([
            SellerProductDataSample(
                seller_product=instance, url=ds['url'], data_type=ds['data_type'], data_format=ds['data_format']
            ) for ds in data_samples
        ])
        SellerProductDataUrl.objects.bulk_create([
            SellerProductDataUrl(
                seller_product=instance, url=du['url'], data_type=du['data_type'], data_format=du['data_format']
            ) for du in data_urls
        ])

        # call for copying instance into archive data
        seller_product_archive = SellerProductArchive()
        seller_product_archive = copy_instance(instance, seller_product_archive)
        seller_product_archive.save()

        return instance
