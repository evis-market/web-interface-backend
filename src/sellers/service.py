import os

from app import exceptions
from app.conf.base import MEDIA_ROOT
from sellers.models import Contact, Seller
from upload.service import UploadService
from users.models import User


class SellerService:
    """ Seller service """
    CONTACTS_NOT_SUPPLIED = 'Contacts are not supplied'

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

        # todo: by some reason serializer couldn't make contacts field to be required;
        #  here is workaround for now
        if not contacts:
            raise exceptions.NotFound(msg=self.CONTACTS_NOT_SUPPLIED)

        seller = Seller.objects.get_seller_by_user_id(user)
        if not seller:
            seller = Seller.objects.create(seller=user, **data)
        else:
            Seller.objects.filter(seller=seller).update(**data)

        if logo_url:
            upload_to = upload_service.get_destination_path(Seller, 'file', logo_url, logo_url.uuid, 'logo_url')
            upload_service.copy_file_from_tmp(logo_url, os.path.join(MEDIA_ROOT, upload_to))
            seller.logo_url = upload_to
            seller.save()

        Contact.objects.delete_all_by_seller(seller)
        Contact.objects.bulk_create([Contact(seller=seller, **contact) for contact in contacts])
