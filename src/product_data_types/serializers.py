from rest_framework import serializers

from product_data_types.models import DataFormat, DataType


class DataTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataType
        fields = [
            'id',
            'name',
        ]


class DataFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataFormat
        fields = [
            'id',
            'name',
        ]
