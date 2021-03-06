from django.db import models


class SellerManager(models.Manager):
    """ Class representing sellers manager """
    def get_seller_by_user_id(self, user_id):
        """ Get seller settings by user_id.
        Returns:
            Seller settings.
        """
        return self.model.objects.filter(seller=user_id).first()


class ContactManager(models.Manager):
    """ Class representing contacts manager """
    def get_all_by_seller(self, seller):
        """ Get seller contacts.
        Returns:
            Seller contacts.
        """
        return self.model.objects.filter(seller=seller)

    def delete_all_by_seller(self, seller_id):
        """ Delete all seller contacts """
        return self.model.objects.filter(seller=seller_id).delete()
