from rest_framework import serializers

from sales.models import Sale


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['created_at', 'uuid', 'seller', 'buyer', 'amount']
