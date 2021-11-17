from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.exceptions import BadRequest
from categories.models import Category
from data_delivery_types.models import DataDeliveryType
from geo_regions.models import GeoRegion
from languages.models import Language
from product_data_types.models import DataFormat, DataType
from seller_products.models import SellerProduct, SellerProductDataSample, SellerProductDataUrl
from sellers.models import Seller
from upload.models import UploadedFile


class CategorySerializer(serializers.ModelSerializer):
    """ Class representing category serializer """

    class Meta:
        model = Category
        fields = ['id', 'name']


class SellerSerializer(serializers.ModelSerializer):
    """ Class representing seller serializer """

    class Meta:
        model = Seller
        fields = ['seller_id', 'name']


class GeoRegionSerializer(serializers.ModelSerializer):
    """ Class representing geo region serializer """

    class Meta:
        model = GeoRegion
        fields = ['id', 'name', 'iso_code']


class LanguageSerializer(serializers.ModelSerializer):
    """ Class representing language serializer """

    class Meta:
        model = Language
        fields = ['id', 'name_native', 'name_en', 'slug']


class DataTypeSerializer(serializers.ModelSerializer):
    """ Class representing data type serializer """

    class Meta:
        model = DataType
        fields = ['id', 'name']


class DataFormatSerializer(serializers.ModelSerializer):
    """ Class representing data format serializer """

    class Meta:
        model = DataFormat
        fields = ['id', 'name']


class DataDeliveryTypeSerializer(serializers.ModelSerializer):
    """ Class representing data delivery type serializer """

    class Meta:
        model = DataDeliveryType
        fields = ['id', 'name']


class DataSampleSerializer(serializers.ModelSerializer):
    """ Class representing data sample serializer

    Attributes:
        data_delivery_type_id (rest_framework.relations.PrimaryKeyRelatedField): data delivery type id
        data_format_id (rest_framework.relations.PrimaryKeyRelatedField): data format id
    """
    data_delivery_type_id = serializers.PrimaryKeyRelatedField(
        queryset=DataDeliveryType.objects.all(), write_only=True, source='data_delivery_type', required=False
    )
    data_format_id = serializers.PrimaryKeyRelatedField(
        queryset=DataFormat.objects.all(), write_only=True, source='data_format', required=False
    )
    file_url = serializers.SerializerMethodField('get_file_url')

    def get_file_url(self, obj):
        return f'{self.context["request"].scheme}://{self.context["request"].get_host()}{obj.file.url}'

    class Meta:
        model = SellerProductDataSample
        fields = ['file_url', 'data_delivery_type_id', 'data_format_id']


class DataUrlsSerializer(serializers.ModelSerializer):
    """ Class representing data urls serializer

    Attributes:
        data_delivery_type_id (rest_framework.relations.PrimaryKeyRelatedField): data delivery type id
        data_format_id (rest_framework.relations.PrimaryKeyRelatedField): data format id
    """
    data_delivery_type_id = serializers.PrimaryKeyRelatedField(queryset=DataDeliveryType.objects.all(), write_only=True,
                                                               source='data_delivery_type')
    data_format_id = serializers.PrimaryKeyRelatedField(queryset=DataFormat.objects.all(), write_only=True,
                                                        source='data_format')

    class Meta:
        model = SellerProductDataUrl
        fields = ['url', 'data_delivery_type_id', 'data_format_id']


class SellerProductsSerializer(serializers.ModelSerializer):
    """ Class representing seller products serializer

    Attributes:
        seller (SellerSerializer): seller
        data_categories_ids (CategorySerializer): data categories ids
        data_geo_regions_ids (GeoRegionSerializer): data geo regions ids
        data_langs_ids (LanguageSerializer): data langs ids
        data_types_ids (DataTypeSerializer): data types ids
        data_formats_ids (DataFormatSerializer): data formats ids
        data_delivery_types_ids (DataDeliveryTypeSerializer): data delivery types ids
        data_samples (DataSampleSerializer): data samples
        data_urls (DataUrlsSerializer): data urls
    """
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
    """ Class representing seller products update serializer

        Attributes:
            seller (rest_framework.relations.PrimaryKeyRelatedField): seller
            data_categories_ids (rest_framework.relations.PrimaryKeyRelatedField): data categories ids
            data_geo_regions_ids (rest_framework.relations.PrimaryKeyRelatedField): data geo regions ids
            data_langs_ids (rest_framework.relations.PrimaryKeyRelatedField): data langs ids
            data_types_ids (rest_framework.relations.PrimaryKeyRelatedField): data types ids
            data_formats_ids (rest_framework.relations.PrimaryKeyRelatedField): data formats ids
            data_delivery_types_ids (rest_framework.relations.PrimaryKeyRelatedField): data delivery types ids
            data_samples (rest_framework.relations.PrimaryKeyRelatedField): data samples
            data_urls (rest_framework.relations.PrimaryKeyRelatedField): data urls
    """
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True)
    data_categories_ids = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True,
                                                             many=True)
    data_geo_regions_ids = serializers.PrimaryKeyRelatedField(queryset=GeoRegion.objects.all(), write_only=True,
                                                              many=True)
    data_langs_ids = serializers.PrimaryKeyRelatedField(queryset=Language.objects.all(), write_only=True, many=True)
    data_types_ids = serializers.PrimaryKeyRelatedField(queryset=DataType.objects.all(), write_only=True, many=True)
    data_formats_ids = serializers.PrimaryKeyRelatedField(queryset=DataFormat.objects.all(), write_only=True, many=True)
    data_delivery_types_ids = serializers.PrimaryKeyRelatedField(queryset=DataDeliveryType.objects.all(),
                                                                 write_only=True, many=True)
    data_samples = serializers.PrimaryKeyRelatedField(queryset=UploadedFile.objects.all(), many=True, required=False)
    data_urls = serializers.ListField(child=DataUrlsSerializer(), write_only=True, required=False)

    def is_valid(self, raise_exception=False):
        if not hasattr(self, '_validated_data'):
            self._errors = {}
            try:
                self._validated_data = self.run_validation(self.initial_data)
            except ValidationError as exc:
                self._validated_data = {}

                if 'descr' in exc.detail and '300' in exc.detail['descr'][0]:
                    exc.detail['descr'] = 'to long, 300 symbols maximum'

                if 'name' in exc.detail and 'blank' in exc.detail['name'][0]:
                    exc.detail['name'] = 'required field'

                if 'data_urls' in exc.detail:
                    for i in exc.detail['data_urls']:
                        if 'url' in exc.detail['data_urls'][i]:
                            exc.detail['data_urls'][i]['url'] = 'URL is invalid'

                # add other errors
                self._errors = exc.detail

        if self._errors and raise_exception:
            raise BadRequest(invalid_fields=self.errors)

        return not bool(self._errors)

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
    """ Class representing seller uploaded files serializer

        Attributes:
            data_samples (rest_framework.relations.PrimaryKeyRelatedField): data samples
    """
    data_samples = serializers.PrimaryKeyRelatedField(queryset=UploadedFile.objects.all(), write_only=True, many=True)
