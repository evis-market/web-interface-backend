from rest_framework import serializers

from data_delivery_types.models import DataDeliveryType


class DataDeliveryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataDeliveryType
        fields = [
            'id',
            'name'
        ]
