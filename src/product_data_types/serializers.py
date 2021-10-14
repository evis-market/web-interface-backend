from rest_framework import serializers

from product_data_types.models import DataFormat, DataType


class DataTypeSerializer(serializers.ModelSerializer):
    """ Class representing serializer for the data type """
    class Meta:
        model = DataType
        fields = [
            'id',
            'name',
        ]


class DataFormatSerializer(serializers.ModelSerializer):
    """ Class representing serializer for the data format """
    class Meta:
        model = DataFormat
        fields = [
            'id',
            'name',
            'data_type_id',
        ]
