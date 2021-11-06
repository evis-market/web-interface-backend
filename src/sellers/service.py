import os

from app.conf.upload import MEDIA_ROOT
from sellers.models import Contact, Seller
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
        logo = data.pop('logo', None)
        upload_service = UploadService()

        seller, _ = Seller.objects.update_or_create(
            seller=user,
            defaults={
                'name': data['name'],
                'descr': data.get('descr', ''),
                'wallet_for_payments_erc20': data.get('wallet_for_payments_erc20', '')
            })

        if logo:
            upload_to = upload_service.get_destination_path(Seller, 'file', logo, logo.uuid, 'logo')
            upload_service.copy_file_from_tmp(logo, os.path.join(MEDIA_ROOT, upload_to))
            seller.logo = upload_to
            seller.save()

        Contact.objects.delete_all_by_seller(seller)
        if contacts:
            Contact.objects.bulk_create([Contact(seller=seller, **contact) for contact in contacts])
