from rest_framework import serializers

from app import validators
from app.exceptions import BadRequest
from sellers.models import Contact, Seller
from upload.models import UploadedFile


class ContactViewSerializer(serializers.ModelSerializer):
    """
    Class representing serializer for contacts
    """

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
    logo_url = serializers.SerializerMethodField('get_logo_url')

    def get_logo_url(self, obj):
        if obj.logo_url:
            return f'{self.context["request"].scheme}://{self.context["request"].get_host()}{obj.logo_url.url}'
        return ''

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


class SellerUpdateSerializer(serializers.ModelSerializer):
    """ Class representing serializer for seller updates

        Attributes:
                contacts (rest_framework.fields.ListField): seller contacts
    """
    contacts = serializers.ListField()
    logo_url = serializers.PrimaryKeyRelatedField(queryset=UploadedFile.objects.all(), required=False)

    def validate(self, data):  # noqa: CCR001
        if not data.get('contacts', None):
            raise BadRequest(invalid_fields={'contacts': {0: 'This field is required'}})

        invalid_fields = {}
        for i, contact in enumerate(data['contacts']):
            if contact['type_id'] == Contact.TYPE_ID_URL and not validators.is_url_valid(contact['value']):
                invalid_fields[i] = 'URL is invalid'
            elif contact['type_id'] == Contact.TYPE_ID_EMAIL and not validators.is_email_valid(contact['value']):
                invalid_fields[i] = 'Email is invalid'
            elif contact['type_id'] == Contact.TYPE_ID_PHONE and not validators.is_phone_valid(contact['value']):
                invalid_fields[i] = 'Phone is invalid'

        if invalid_fields:
            raise BadRequest(invalid_fields={'contacts': invalid_fields})

        return data

    class Meta:
        model = Seller
        fields = [
            'name',
            'descr',
            'logo_url',
            'wallet_for_payments_erc20',
            'contacts',
        ]
