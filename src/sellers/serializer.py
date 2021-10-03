from rest_framework import serializers

from sellers.models import Contact, Seller


class ContactViewSerializer(serializers.ModelSerializer):
    type_id = serializers.ReadOnlyField(source='type')

    class Meta:
        model = Contact
        fields = (
            'type_id',
            'value',
            'comment',
        )


class SellerViewSerializer(serializers.ModelSerializer):
    contacts = ContactViewSerializer(many=True)
    user_id = serializers.ReadOnlyField(source='seller.user_id')

    class Meta:
        model = Seller
        fields = (
            'user_id',
            'name',
            'descr',
            'logo_url',
            'wallet_for_payments_erc20',
            'rating',
            'contacts',
        )


class ContactUpdateSerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(source='type')

    class Meta:
        model = Contact
        fields = (
            'type_id',
            'value',
            'comment',
        )


class SellerUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    descr = serializers.CharField(required=False)
    logo_url = serializers.URLField(required=False)
    wallet_for_payments_erc20 = serializers.CharField(required=False)
    contacts = ContactUpdateSerializer(many=True)
