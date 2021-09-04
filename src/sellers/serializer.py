from rest_framework import serializers

from sellers.models import Contact, Seller


class ContactViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'seller_id',
            'type_id',
            'value',
            'comment',
        )


class SellerViewSerializer(serializers.ModelSerializer):
    contacts = ContactViewSerializer(many=True)

    class Meta:
        model = Seller
        fields = (
            'id',
            'seller_id',
            'name',
            'description',
            'logo_url',
            'wallet_for_payments_erc20',
            'rating',
            'contacts',
        )


class ContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'type_id',
            'value',
            'comment',
        )


class SellerUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    logo_url = serializers.URLField(required=False)
    wallet_for_payments_erc20 = serializers.CharField(required=False)
    contacts = ContactUpdateSerializer(many=True)
