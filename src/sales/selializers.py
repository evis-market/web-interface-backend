from rest_framework import serializers

from sales.models import Sale


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['created_at', 'uuid', 'seller_user_id', 'buyer_user_id', 'amount']
