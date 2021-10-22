from rest_framework import serializers

from sellers.models import Contact, Seller


class ContactViewSerializer(serializers.ModelSerializer):
    """ Class representing serializer for contacts

        Attributes:
                type_id (rest_framework.fields.ReadOnlyField): type of contact
    """
    type_id = serializers.ReadOnlyField(source='type')

    class Meta:
        model = Contact
        fields = (
            'type_id',
            'value',
            'comment',
        )


class SellerViewSerializer(serializers.ModelSerializer):
    """ Class representing serializer for sellers

        Attributes:
                contacts (src.sellers.serializer): seller contacts
                user_id (rest_framework.fields.ReadOnlyField): seller user id
    """
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
    """ Class representing serializer for contact updates

        Attributes:
                type_id (rest_framework.fields.IntegerField): type of contact
    """
    type_id = serializers.IntegerField(source='type')

    class Meta:
        model = Contact
        fields = (
            'type_id',
            'value',
            'comment',
        )


class SellerUpdateSerializer(serializers.ModelSerializer):
    """ Class representing serializer for seller updates

        Attributes:
                contacts (rest_framework.fields.ListField): seller contacts
    """
    contacts = serializers.ListField(child=ContactUpdateSerializer(), write_only=True, required=True)

    class Meta:
        model = Seller
        fields = [
            'name',
            'descr',
            'logo_url',
            'wallet_for_payments_erc20',
            'contacts',
        ]
