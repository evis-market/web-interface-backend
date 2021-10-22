from rest_framework import serializers

from data_delivery_types.models import DataDeliveryType


class DataDeliveryTypeSerializer(serializers.ModelSerializer):
    """ Class representing serializer for the data delivery type """
    class Meta:
        model = DataDeliveryType
        fields = [
            'id',
            'name'
        ]
