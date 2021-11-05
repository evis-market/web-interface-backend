import os

from app import exceptions
from app.conf.upload import MEDIA_ROOT
from sellers.models import Contact, Seller
from upload.models import UploadedFile
from upload.service import UploadService
from users.models import User


class SellerService:
    """ Seller service """

    def create_or_update_object(self, user: User, data: dict) -> None:
        """ Creates or updates object.

            Args:
                user (src.users.models.User): user
                data (dict): params dict

            Attributes:
                contacts (list): contact list
        """
        contacts = data.pop('contacts', None)
        logo_url = data.pop('logo_url', None)
        upload_service = UploadService()

        seller, _ = Seller.objects.update_or_create(
            seller=user,
            defaults={'name': data['name'],
                      'description': data.get('description', ''),
                      'wallet_for_payments_erc20': data.get('wallet_for_payments_erc20', '')})

        if logo_url:
            upload_to = upload_service.get_destination_path(Seller, 'file', logo_url, logo_url.uuid, 'logo_url')
            upload_service.copy_file_from_tmp(logo_url, os.path.join(MEDIA_ROOT, upload_to))
            seller.logo_url = upload_to
            seller.save()

        if contacts:
            Contact.objects.delete_all_by_seller(seller)
            Contact.objects.bulk_create([Contact(seller=seller, **contact) for contact in contacts])
